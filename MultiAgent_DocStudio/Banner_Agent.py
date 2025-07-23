from jinja2 import Template
from llm_summarizer import LLMSummarizer

def render_banner_agent(st, llm_provider, llm_model_key):
    st.markdown('<div style="padding-bottom:1.5rem;"><h2 style="color:#111;">Banner/Post Generator Agent</h2></div>', unsafe_allow_html=True)
    with st.sidebar:
        st.header("Banner/Post Settings 🖼️")
        platform = st.selectbox("Target Platform", ["Instagram", "Facebook", "LinkedIn", "Twitter", "Custom"], index=0)
        style = st.selectbox("Style", ["Bold & Catchy", "Minimalist", "Professional", "Playful"], index=0)
    st.markdown('<div class="text-card">', unsafe_allow_html=True)
    st.markdown("<h3>Enter Banner/Post Details</h3>", unsafe_allow_html=True)
    campaign_brief = st.text_area("Campaign Brief", key="banner_campaign_brief")
    key_message = st.text_input("Key Message", key="banner_key_message")
    generate_btn = st.button("Generate Banner/Post", key="generate_banner_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    banner_template = Template("""
Create a social media banner or post for the following campaign.

**Campaign Brief:** {{ campaign_brief }}
**Target Platform:** {{ platform }}
**Key Message:** {{ key_message }}
**Style:** {{ style }}

- Make it visually engaging and concise.
- Include a strong call to action.
- Suggest relevant hashtags.
- Output only the text/copy for the banner/post.
""")

    if generate_btn:
        if not campaign_brief or not key_message:
            st.warning("Please fill in all fields to generate a banner/post.")
        else:
            prompt = banner_template.render(
                campaign_brief=campaign_brief,
                platform=platform,
                key_message=key_message,
                style=style
            )
            try:
                llm_summarizer = LLMSummarizer(provider=llm_provider, model=llm_model_key)
                with st.spinner("Generating banner/post content..."):
                    content = llm_summarizer.generate(prompt)
                st.success("Banner/Post generated!")
                st.markdown("<h4>Generated Banner/Post</h4>", unsafe_allow_html=True)
                st.text_area("Generated Banner/Post", value=content, height=200, key="generated_banner_content_area")
                st.download_button("Download as TXT", data=content, file_name="generated_banner_post.txt")
            except Exception as e:
                st.error(f"Error generating banner/post: {str(e)}") 