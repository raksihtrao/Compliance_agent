import streamlit as st
import os
import tiktoken
from datetime import datetime
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from llm_summarizer import LLMSummarizer
from storage_manager import StorageManager
from compliance_agent import ComplianceAgent
from urllib.parse import parse_qs
from prompt_db import PromptDB
from compliance_chatbot import ComplianceChatbot


load_dotenv()

if 'active_agent' not in st.session_state:
    st.session_state['active_agent'] = 'summarizer'

st.set_page_config(
    page_title="DocStudio",
    #page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.upload-card, .text-card {
    background: #fff;
    border: 2px dashed #bfc9d8;
    border-radius: 18px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.upload-card h2, .text-card h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.upload-card p, .text-card p {
    color: #6c7a89;
    margin-bottom: 1.5rem;
}
.section-sep {
    margin: 2.5rem 0 2rem 0;
    border: none;
    border-top: 2px dashed #e0e6ef;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.stButton > button {
    border-radius: 999px !important;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    padding: 0.85rem 2.5rem !important;
    margin: 0 0.5rem 0.5rem 0 !important;
    border: 2px solid #111 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
    transition: background 0.2s, color 0.2s;
}
.stButton > button.selected {
    background: #111 !important;
    color: #fff !important;
    border: 2px solid #111 !important;
}
.stButton > button.unselected {
    background: #fff !important;
    color: #111 !important;
    border: 2px solid #111 !important;
}
</style>
""", unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    btn1 = st.button('Summarizer Agent', key='nav_summarizer', use_container_width=True)
    if btn1:
        st.session_state['active_agent'] = 'summarizer'
with nav_col2:
    btn2 = st.button('Compliance Check Agent', key='nav_compliance', use_container_width=True)
    if btn2:
        st.session_state['active_agent'] = 'compliance'


active_agent = st.session_state['active_agent']
st.markdown(f"""
<script>
const btns = window.parent.document.querySelectorAll('.stButton > button');
if (btns.length >= 2) {{
    btns[0].classList.remove('selected','unselected');
    btns[1].classList.remove('selected','unselected');
    if ('{active_agent}' === 'summarizer') {{
        btns[0].classList.add('selected');
        btns[1].classList.add('unselected');
    }} else {{
        btns[0].classList.add('unselected');
        btns[1].classList.add('selected');
    }}
}}
</script>
""", unsafe_allow_html=True)
st.markdown("<hr style='margin-bottom:2rem;'>", unsafe_allow_html=True)


if st.session_state['active_agent'] == 'summarizer':
    st.markdown('<div style="padding-bottom:1.5rem;"><h2 style="color:#111;">Summarizer Agent</h2></div>', unsafe_allow_html=True)
    document_processor = DocumentProcessor()
    llm_summarizer = LLMSummarizer()
    storage_manager = StorageManager()
    with st.sidebar:
        st.header("Summarization Configuration 🛠️")
        st.markdown(
            "<span style='color:#2563eb;font-weight:600;'>Adjust how your summaries are generated!!</span>",
            unsafe_allow_html=True
        )
        summary_length = st.selectbox("Summary Length", ["Short (100-200 words)", "Medium (200-400 words)", "Long (400-600 words)"], index=1)
        storage_type = st.selectbox("Storage Type", ["JSON", "CSV", "SQLite Database"], index=2)
    st.markdown('<div class="text-card">', unsafe_allow_html=True)
    st.markdown("<h2>Paste or Type Text</h2>", unsafe_allow_html=True)
    st.markdown("<p>Paste your document or text below</p>", unsafe_allow_html=True)
    user_text = st.text_area("Paste your text here...", height=300, key="user_text_area")
    col1, col2 = st.columns([1, 1])
    with col1:
        summarize_text_btn = st.button("Summarize Text", key="summarize_text_btn", help="Generate a summary for this text.", use_container_width=True)
    with col2:
        takeaway_text_btn = st.button("Key Takeaway", key="takeaway_text_btn", help="Get up to 5 key takeaways for this text.", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="section-sep">', unsafe_allow_html=True)
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("<h2>Upload Documents</h2>", unsafe_allow_html=True)
    st.markdown("<p>Upload PDF, Word, Excel, or Text files for summarization and key takeaways.</p>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop files here or click to browse",
        type=["pdf", "txt", "xlsx", "csv", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    col3, col4 = st.columns([1, 1])
    with col3:
        summarize_file_btn = st.button("Summarize Text", key="summarize_file_btn", help="Generate a summary for uploaded document(s).", use_container_width=True)
    with col4:
        takeaway_file_btn = st.button("Key Takeaway", key="takeaway_file_btn", help="Get up to 5 key takeaways for uploaded document(s).", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if summarize_text_btn or takeaway_text_btn:
        if not user_text or not user_text.strip():
            st.warning("Please paste or type some text to summarize or extract key takeaways.")
        else:
            word_count = len(user_text.split())
            st.write(f"**Word Count:** {word_count:,}")
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  
            token_count = len(encoding.encode(user_text))
            st.write(f"**Estimated Tokens:** {token_count:,}")
            with st.expander("View Input Text"):
                st.text_area("Input Text", value=user_text[:1000] + ("..." if len(user_text) > 1000 else ""), height=200, disabled=True)
            if summarize_text_btn:
                with st.spinner("Generating summary..."):
                    try:
                        summary = llm_summarizer.summarize(
                            text=user_text,
                            length=summary_length
                        )
                        if summary:
                            st.success("Summary generated!")
                            st.markdown(f"**Summary:**\n\n{summary}")
                            summary_data = {
                                'filename': 'user_input.txt',
                                'file_type': 'text/plain',
                                'file_size_kb': len(user_text.encode('utf-8')) / 1024,
                                'original_word_count': word_count,
                                'summary': summary,
                                'summary_word_count': len(summary.split()),
                                'model_used': "gpt-3.5-turbo (openai)",
                                'summary_length': summary_length,
                                'date': datetime.now().isoformat(),
                                'extracted_text': user_text[:500] + ("..." if len(user_text) > 500 else user_text)
                            }
                            if storage_type == "JSON":
                                storage_manager.save_to_json(summary_data)
                            elif storage_type == "CSV":
                                storage_manager.save_to_csv(summary_data)
                            else:
                                storage_manager.save_to_sqlite(summary_data)
                            st.info("Summary saved!")
                        else:
                            st.error("Failed to generate summary.")
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
            if takeaway_text_btn:
                with st.spinner("Generating key takeaways..."):
                    try:
                        takeaways = llm_summarizer.key_takeaways(user_text)
                        if takeaways:
                            st.success("Key takeaways generated!")
                            st.markdown("**Key Takeaways:**")
                            st.markdown("\n".join([f"- {line}" for line in takeaways]))
                        else:
                            st.error("Failed to generate key takeaways.")
                    except Exception as e:
                        st.error(f"Error generating key takeaways: {str(e)}")
    if summarize_file_btn or takeaway_file_btn:
        if not uploaded_files:
            st.warning("Please upload at least one document to summarize or extract key takeaways.")
        else:
            st.markdown("<h4 style='margin-top:2rem;'>Uploaded Document Actions</h4>", unsafe_allow_html=True)
            for idx, uploaded_file in enumerate(uploaded_files):
                st.markdown('<div class="file-card" style="background:#f7f9fa;border-radius:12px;padding:1.5rem 1rem;margin-bottom:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
                st.markdown(f"<h4>📄 {uploaded_file.name}</h4>", unsafe_allow_html=True)
                file_size = len(uploaded_file.getvalue()) / 1024  # KB
                st.write(f"**Size:** {file_size:.1f} KB | **Type:** {uploaded_file.type}")
                try:
                    extracted_text = document_processor.extract_text(uploaded_file)
                    word_count = len(extracted_text.split())
                    st.write(f"**Word Count:** {word_count:,}")
                    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
                    token_count = len(encoding.encode(extracted_text))
                    st.write(f"**Estimated Tokens:** {token_count:,}")
                    with st.expander("View Extracted Text"):
                        st.text_area("Extracted Text", value=extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""), height=200, disabled=True)
                    if summarize_file_btn:
                        with st.spinner("Generating summary..."):
                            try:
                                summary = llm_summarizer.summarize(
                                    text=extracted_text,
                                    length=summary_length
                                )
                                if summary:
                                    st.success("Summary generated!")
                                    st.markdown(f"**Summary:**\n\n{summary}")
                                    summary_data = {
                                        'filename': uploaded_file.name,
                                        'file_type': uploaded_file.type,
                                        'file_size_kb': file_size,
                                        'original_word_count': word_count,
                                        'summary': summary,
                                        'summary_word_count': len(summary.split()),
                                        'model_used': "gpt-3.5-turbo (openai)",
                                        'summary_length': summary_length,
                                        'date': datetime.now().isoformat(),
                                        'extracted_text': extracted_text[:500] + ("..." if len(extracted_text) > 500 else extracted_text)
                                    }
                                    if storage_type == "JSON":
                                        storage_manager.save_to_json(summary_data)
                                    elif storage_type == "CSV":
                                        storage_manager.save_to_csv(summary_data)
                                    else:
                                        storage_manager.save_to_sqlite(summary_data)
                                    st.info("Summary saved!")
                                else:
                                    st.error("Failed to generate summary.")
                            except Exception as e:
                                st.error(f"Error generating summary: {str(e)}")
                    if takeaway_file_btn:
                        with st.spinner("Generating key takeaways with Ollama Mistral..."):
                            try:
                                takeaways = llm_summarizer.key_takeaways(extracted_text)
                                if takeaways:
                                    st.success("Key takeaways generated!")
                                    st.markdown("**Key Takeaways:**")
                                    st.markdown("\n".join([f"- {line}" for line in takeaways]))
                                else:
                                    st.error("Failed to generate key takeaways.")
                            except Exception as e:
                                st.error(f"Error generating key takeaways: {str(e)}")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
else:
   
    with st.sidebar:
        st.markdown('<h3>Compliance Chatbot</h3>', unsafe_allow_html=True)
        if 'compliance_chat_history' not in st.session_state:
            st.session_state['compliance_chat_history'] = []
        if 'compliance_chat_input' not in st.session_state:
            st.session_state['compliance_chat_input'] = ''
        
        st.markdown("""
        <style>
        .chat-bubble-user {
            background: #2563eb;
            color: #fff;
            border-radius: 18px 18px 4px 18px;
            padding: 0.8em 1.2em;
            margin: 0.5em 0 0.5em 2em;
            max-width: 85%;
            text-align: left;
            font-size: 1.05em;
            box-shadow: 0 2px 8px rgba(37,99,235,0.08);
        }
        .chat-bubble-bot {
            background: #f3f4f6;
            color: #222;
            border-radius: 18px 18px 18px 4px;
            padding: 0.8em 1.2em;
            margin: 0.5em 2em 0.5em 0;
            max-width: 85%;
            text-align: left;
            font-size: 1.05em;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .chat-row {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
        }
        .chat-row.user {
            justify-content: flex-end;
        }
        .chat-row.bot {
            justify-content: flex-start;
        }
        </style>
        """, unsafe_allow_html=True)
        for msg in st.session_state['compliance_chat_history']:
            if msg['role'] == 'user':
                st.markdown(f"<div class='chat-row user'><div class='chat-bubble-user'>🧑 {msg['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-row bot'><div class='chat-bubble-bot'>🤖 {msg['content']}</div></div>", unsafe_allow_html=True)
        
        chat_col1 = st.container()
        chat_col2, chat_col3 = st.columns([1,1])
        with chat_col1:
            chatbot_input = st.text_input('Ask a compliance question...', key='compliance_chat_input', label_visibility='collapsed', on_change=None)
        with chat_col2:
            send_clicked = st.button('Send', key='compliance_chat_send', use_container_width=True, help='Send your message', type='primary')
        with chat_col3:
            clear_chat_pressed = st.button('Clear Chat', key='clear_compliance_chat', help='Clear the chat history', type='secondary')
        if clear_chat_pressed:
            st.session_state['compliance_chat_history'] = []
            if 'compliance_chat_input' in st.session_state:
                del st.session_state['compliance_chat_input']
            st.experimental_rerun()
        if send_clicked:
            if chatbot_input.strip():
                st.session_state['compliance_chat_history'].append({'role': 'user', 'content': chatbot_input})
                context = st.session_state.get('compliance_prompt', None)
                try:
                    chatbot = ComplianceChatbot()
                    bot_response = chatbot.ask(chatbot_input, context=context)
                except Exception as e:
                    bot_response = f"[Error from LLM: {e}]"
                st.session_state['compliance_chat_history'].append({'role': 'bot', 'content': bot_response})
                
                st.experimental_set_query_params(dummy=str(send_clicked))
                st.session_state.pop('compliance_chat_input', None)
                st.rerun()
    
    with st.container():
        st.markdown('<div class="text-card">', unsafe_allow_html=True)
        st.markdown("<h3>Compliance Check Prompt Builder</h3>", unsafe_allow_html=True)
       
        if 'protocol_name' not in st.session_state:
            st.session_state['protocol_name'] = ''
        if 'protocol_description' not in st.session_state:
            st.session_state['protocol_description'] = ''
        if 'what_to_flag' not in st.session_state:
            st.session_state['what_to_flag'] = ''
        if 'severity_threshold' not in st.session_state:
            st.session_state['severity_threshold'] = 'Medium'
        if 'output_format' not in st.session_state:
            st.session_state['output_format'] = 'Summary'
        if 'citation_required' not in st.session_state:
            st.session_state['citation_required'] = True
        if 'language' not in st.session_state:
            st.session_state['language'] = 'English'
        protocol_name = st.text_input("Compliance Protocol Name", 
                                     value=st.session_state['protocol_name'],
                                     key='protocol_name_input',
                                     help="e.g., 'GDPR Data Minimization', 'HIPAA PHI Handling'")
        protocol_description = st.text_area("Protocol Description / Rule", 
                                           value=st.session_state['protocol_description'],
                                           key='protocol_description_input',
                                           help="Define the rule or guideline the document should follow", 
                                           height=120)
        what_to_flag = st.text_input("What to Flag", 
                                    value=st.session_state['what_to_flag'],
                                    key='what_to_flag_input',
                                    help="e.g., 'Unencrypted PII', 'Unauthorized third-party sharing'")
        severity_threshold = st.selectbox("Severity Threshold", 
                                        ["Low", "Medium", "High"], 
                                        index=["Low", "Medium", "High"].index(st.session_state['severity_threshold']),
                                        key='severity_threshold_input',
                                        help="How strict should the check be?")
        output_format = st.selectbox("Expected Output Format", 
                                    ["Summary", "JSON", "Checklist", "Bullet List"], 
                                    index=["Summary", "JSON", "Checklist", "Bullet List"].index(st.session_state['output_format']),
                                    key='output_format_input')
        citation_required = st.toggle("Citation Required?", 
                                     value=st.session_state['citation_required'],
                                     key='citation_required_input',
                                     help="Should the LLM cite specific clauses/laws?")
        language = st.selectbox("Language of Document", 
                               ["English", "Spanish", "French", "German", "Chinese", "Other"], 
                               index=["English", "Spanish", "French", "German", "Chinese", "Other"].index(st.session_state['language']),
                               key='language_input')
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h4>Prompt Preview</h4>", unsafe_allow_html=True)
        st.code(f"""
Compliance Protocol: {protocol_name}
Description/Rule: {protocol_description}
What to Flag: {what_to_flag}
Severity Threshold: {severity_threshold}
Expected Output Format: {output_format}
Citation Required: {'Yes' if citation_required else 'No'}
Language: {language}
""", language="markdown")
       
        st.markdown("""
        <style>
        .purple-btn button {
            background: #6C1AC4 !important;
            color: #fff !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 0.7rem 2.2rem !important;
            border: none !important;
            margin-right: 1rem !important;
            box-shadow: 0 2px 8px rgba(108,26,196,0.08) !important;
            transition: background 0.2s, color 0.2s;
        }
        .reset-btn button {
            background: #fff !important;
            color: #7b2ff2 !important;
            border: 2px solid #7b2ff2 !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 0.7rem 2.2rem !important;
            margin-right: 0.5rem !important;
            box-shadow: 0 2px 8px rgba(123,47,242,0.04) !important;
            transition: background 0.2s, color 0.2s;
        }
        </style>
        """, unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1,1])
        with btn_col1:
            done_clicked = st.button('Done', key='compliance_prompt_done_btn', help='Lock in prompt and proceed to upload', use_container_width=True, type='primary')
        with btn_col2:
            reset_clicked = st.button('Reset', key='compliance_prompt_reset', help='Clear all fields', use_container_width=True)
        st.markdown('<div class="purple-btn"></div>', unsafe_allow_html=True)
        st.markdown('<div class="reset-btn"></div>', unsafe_allow_html=True)
        if reset_clicked:
            
            st.session_state['protocol_name'] = ''
            st.session_state['protocol_description'] = ''
            st.session_state['what_to_flag'] = ''
            st.session_state['severity_threshold'] = 'Medium'
            st.session_state['output_format'] = 'Summary'
            st.session_state['citation_required'] = True
            st.session_state['language'] = 'English'
            
            st.session_state['compliance_prompt_done'] = False
            
            if 'compliance_prompt' in st.session_state:
                del st.session_state['compliance_prompt']
            st.success("Form fields have been reset!")
            st.rerun()
        if done_clicked:
            st.session_state['compliance_prompt_done'] = True
            st.session_state['compliance_prompt'] = f"""
Compliance Protocol: {protocol_name}
Description/Rule: {protocol_description}
What to Flag: {what_to_flag}
Severity Threshold: {severity_threshold}
Expected Output Format: {output_format}
Citation Required: {'Yes' if citation_required else 'No'}
Language: {language}
"""
            
            st.session_state['protocol_name'] = protocol_name
            st.session_state['protocol_description'] = protocol_description
            st.session_state['what_to_flag'] = what_to_flag
            st.session_state['severity_threshold'] = severity_threshold
            st.session_state['output_format'] = output_format
            st.session_state['citation_required'] = citation_required
            st.session_state['language'] = language
           
            prompt_db = PromptDB()
            prompt_db.save_prompt(
                protocol_name,
                protocol_description,
                what_to_flag,
                severity_threshold,
                output_format,
                citation_required,
                language
            )
        if st.session_state.get('compliance_prompt_done', False):
            st.success('Prompt locked in! Please upload your document(s) below for compliance checking.')
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-sep">', unsafe_allow_html=True)
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("<h3>Upload Documents</h3>", unsafe_allow_html=True)
    compliance_files = st.file_uploader(
        "Drop files here or click to browse",
        type=["pdf", "txt", "docx", "md", "json"],
        accept_multiple_files=True,
        key="compliance_file_uploader",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="section-sep">', unsafe_allow_html=True)
    st.markdown('<div class="text-card">', unsafe_allow_html=True)
    domain = st.selectbox("Select Compliance Domain", ["GDPR", "HIPAA", "SOC 2", "ISO 27001", "PCI-DSS"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)
    run_check = st.button("Run Compliance Check", use_container_width=True)
    if run_check:
        if not st.session_state.get('compliance_prompt_done', False):
            st.error("Please complete the compliance prompt builder first by clicking 'Done'.")
        else:
            with st.spinner(f"Running compliance check for {domain}..."):
                try:
                    agent = ComplianceAgent(domain=domain)
                    
                    all_text = ''
                    if compliance_files:
                        from document_processor import DocumentProcessor
                        processor = DocumentProcessor()
                        for f in compliance_files:
                            try:
                                all_text += "\n\n" + processor.extract_text(f)
                            except Exception as e:
                                st.error(f"Error extracting text from {f.name}: {e}")
                    
                    if not all_text.strip():
                        st.warning("Please provide text or upload a document.")
                    else:
                       
                        compliance_prompt = st.session_state.get('compliance_prompt', '')
                        results = agent.check_compliance(all_text, custom_prompt=compliance_prompt)
                        
                        
                        st.success(f" Compliance check complete for {domain}")
                        
                        
                        with st.expander(" View Compliance Protocol Used"):
                            st.markdown("**Compliance Protocol Details:**")
                            st.code(compliance_prompt, language="markdown")
                        
                        
                        st.markdown("""
                        <style>
                        .compliance-card {
                            background: #fff;
                            border-radius: 16px;
                            padding: 2rem;
                            margin: 1.5rem 0;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                            border-left: 4px solid #10b981;
                        }
                        .violation-card {
                            background: #fff;
                            border-radius: 16px;
                            padding: 2rem;
                            margin: 1.5rem 0;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                            border-left: 4px solid #ef4444;
                        }
                        .approval-card {
                            background: #fff;
                            border-radius: 16px;
                            padding: 2rem;
                            margin: 1.5rem 0;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                            border-left: 4px solid #3b82f6;
                        }
                        .summary-card {
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            border-radius: 16px;
                            padding: 2rem;
                            margin: 1.5rem 0;
                            box-shadow: 0 8px 32px rgba(102,126,234,0.3);
                        }
                        .metric-box {
                            background: #f8fafc;
                            border-radius: 12px;
                            padding: 1.5rem;
                            margin: 1rem 0;
                            border: 1px solid #e2e8f0;
                        }
                        .status-badge {
                            display: inline-block;
                            padding: 0.5rem 1rem;
                            border-radius: 999px;
                            font-weight: 600;
                            font-size: 0.875rem;
                            margin: 0.25rem;
                        }
                        .status-compliant { background: #dcfce7; color: #166534; }
                        .status-violation { background: #fee2e2; color: #991b1b; }
                        .status-warning { background: #fef3c7; color: #92400e; }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        
                        for idx, result in enumerate(results):
                            st.markdown(f"<h3> Analysis Result {idx+1}</h3>", unsafe_allow_html=True)
                            
                            if isinstance(result, dict):
                                
                                if 'compliance_summary' in result:
                                    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                                    st.markdown(f"<h4> Compliance Summary</h4>", unsafe_allow_html=True)
                                    st.markdown(f"<p>{result['compliance_summary']}</p>", unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                
                                if 'approvals' in result and result['approvals']:
                                    st.markdown('<div class="approval-card">', unsafe_allow_html=True)
                                    st.markdown(f"<h4> Compliant Points</h4>", unsafe_allow_html=True)
                                    if isinstance(result['approvals'], list):
                                        for i, approval in enumerate(result['approvals'], 1):
                                            st.markdown(f"<div class='metric-box'><strong>{i}.</strong> {approval}</div>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<div class='metric-box'>{result['approvals']}</div>", unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                
                                if 'violations' in result and result['violations']:
                                    st.markdown('<div class="violation-card">', unsafe_allow_html=True)
                                    st.markdown(f"<h4> Compliance Violations</h4>", unsafe_allow_html=True)
                                    if isinstance(result['violations'], list):
                                        for i, violation in enumerate(result['violations'], 1):
                                            st.markdown(f"<div class='metric-box'><strong>{i}.</strong> {violation}</div>", unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<div class='metric-box'>{result['violations']}</div>", unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                
                                other_fields = {k: v for k, v in result.items() 
                                              if k not in ['compliance_summary', 'approvals', 'violations']}
                                if other_fields:
                                    st.markdown('<div class="compliance-card">', unsafe_allow_html=True)
                                    st.markdown(f"<h4> Additional Information</h4>", unsafe_allow_html=True)
                                    for field_name, field_value in other_fields.items():
                                        st.markdown(f"<div class='metric-box'>", unsafe_allow_html=True)
                                        st.markdown(f"<strong>{field_name.replace('_', ' ').title()}:</strong>", unsafe_allow_html=True)
                                        if isinstance(field_value, list):
                                            for item in field_value:
                                                st.markdown(f"• {item}", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<p>{field_value}</p>", unsafe_allow_html=True)
                                        st.markdown("</div>", unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                            
                            else:
                                # Fallback for non-dict results
                                st.markdown('<div class="compliance-card">', unsafe_allow_html=True)
                                st.markdown(f"<h4> Raw Result</h4>", unsafe_allow_html=True)
                                st.markdown(f"<div class='metric-box'>{result}</div>", unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            
                            if idx < len(results) - 1:
                                st.markdown("<hr style='margin: 2rem 0; border: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)
                        
                        
                        if results:
                            st.markdown("<h3> Overall Compliance Assessment</h3>", unsafe_allow_html=True)
                            
                            
                            total_violations = 0
                            total_approvals = 0
                            
                            for result in results:
                                if isinstance(result, dict):
                                    if 'violations' in result:
                                        if isinstance(result['violations'], list):
                                            total_violations += len(result['violations'])
                                        else:
                                            total_violations += 1
                                    if 'approvals' in result:
                                        if isinstance(result['approvals'], list):
                                            total_approvals += len(result['approvals'])
                                        else:
                                            total_approvals += 1
                            
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Violations", total_violations, delta=None)
                            with col2:
                                st.metric("Compliant Points", total_approvals, delta=None)
                            with col3:
                                compliance_score = "🟢 Compliant" if total_violations == 0 else "🔴 Non-Compliant" if total_violations > 3 else "🟡 Needs Review"
                                st.metric("Overall Status", compliance_score, delta=None)
                            
                            # Add recommendations
                            if total_violations > 0:
                                st.warning(f"⚠️ **Action Required:** {total_violations} compliance issue(s) found. Please review and address the violations listed above.")
                            else:
                                st.success("🎉 **Excellent!** No compliance violations detected. Your document appears to meet the specified requirements.")
                            
                            # Save results section
                            st.markdown("<h3>💾 Save Results</h3>", unsafe_allow_html=True)
                            
                            # Create comprehensive report data
                            report_data = {
                                'domain': domain,
                                'protocol_name': st.session_state.get('protocol_name', ''),
                                'protocol_description': st.session_state.get('protocol_description', ''),
                                'analysis_date': datetime.now().isoformat(),
                                'total_violations': total_violations,
                                'total_approvals': total_approvals,
                                'overall_status': "Compliant" if total_violations == 0 else "Non-Compliant" if total_violations > 3 else "Needs Review",
                                'results': results,
                                'files_analyzed': [f.name for f in compliance_files] if compliance_files else ['text_input']
                            }
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("💾 Save as JSON", key="save_json_btn"):
                                    try:
                                        storage_manager = StorageManager()
                                        filename = f"compliance_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                                        storage_manager.save_to_json(report_data, filename)
                                        st.success(f" Report saved as {filename}")
                                    except Exception as e:
                                        st.error(f"Error saving report: {e}")
                            
                            with col2:
                                if st.button(" Save to Database", key="save_db_btn"):
                                    try:
                                        storage_manager = StorageManager()
                                        storage_manager.save_to_sqlite(report_data)
                                        st.success(" Report saved to database")
                                    except Exception as e:
                                        st.error(f"Error saving to database: {e}")
                            
                            with col3:
                                if st.button(" Download Report", key="download_btn"):
                                    try:
                                        import json
                                        report_json = json.dumps(report_data, indent=2)
                                        st.download_button(
                                            label="📥 Download JSON",
                                            data=report_json,
                                            file_name=f"compliance_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                            mime="application/json"
                                        )
                                    except Exception as e:
                                        st.error(f"Error creating download: {e}")
                except Exception as e:
                    st.error(f"Error running compliance check: {str(e)}")
                    st.info("Please check that Ollama is running and the Mistral model is available.") 