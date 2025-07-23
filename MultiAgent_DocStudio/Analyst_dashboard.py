import pandas as pd
from jinja2 import Template
from llm_summarizer import LLMSummarizer
import streamlit as st

def render_analyst_dashboard(st, llm_provider, llm_model_key):
    st.markdown('<div style="padding-bottom:1.5rem;"><h2 style="color:#111;">Campaign Performance Analyst Agent</h2></div>', unsafe_allow_html=True)
    with st.sidebar:
        st.header("Analysis Settings 📊")
        analysis_type = st.selectbox("Analysis Type", ["Summary & Insights", "Recommendations", "Anomaly Detection"], index=0)
        goal = st.text_input("Campaign Goal (optional)", key="analyst_goal")
    st.markdown('<div class="text-card">', unsafe_allow_html=True)
    st.markdown("<h3>Upload Campaign Data</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"], key="analyst_file_uploader")
    analyze_btn = st.button("Analyze Campaign", key="analyze_campaign_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not uploaded_file:
            st.warning("Please upload a campaign data file.")
            return
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return
        st.markdown("<h4>Preview of Uploaded Data</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(20))
        # Prepare prompt for LLM
        prompt_template = Template("""
You are a marketing analytics expert. Analyze the following campaign data and provide:
- A concise summary of key metrics and trends
- Actionable insights
- Recommendations to improve performance
{% if analysis_type == 'Anomaly Detection' %}- Detect and explain any anomalies or outliers
{% endif %}
{% if goal %}- Consider the campaign goal: {{ goal }}
{% endif %}

Data (CSV):
{{ data_csv }}
""")
        data_csv = df.to_csv(index=False)
        prompt = prompt_template.render(
            analysis_type=analysis_type,
            goal=goal,
            data_csv=data_csv
        )
        try:
            llm_summarizer = LLMSummarizer(provider=llm_provider, model=llm_model_key)
            with st.spinner("Analyzing campaign data with LLM..."):
                analysis = llm_summarizer.generate(prompt)
            st.success("Analysis complete!")
            st.markdown("<h4>LLM Analysis & Recommendations</h4>", unsafe_allow_html=True)
            st.text_area("Analysis Output", value=analysis, height=400, key="analyst_output_area")
        except Exception as e:
            st.error(f"Error analyzing campaign: {str(e)}") 