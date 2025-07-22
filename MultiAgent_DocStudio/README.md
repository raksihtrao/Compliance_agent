# DocStudio

This project is a document summarization and compliance checking tool with a modern Streamlit web interface. It allows users to upload documents, generate AI-powered summaries, and check for compliance with regulations such as GDPR and HIPAA.

## Features

- Upload and process PDF, TXT, Excel, CSV, and Word documents
- Generate summaries using OpenAI's GPT models (GPT-3.5, GPT-4)
- Save summaries to JSON, CSV, or SQLite database
- Search and manage a knowledge base of document summaries
- View usage statistics and summary analytics
- Estimate API costs before processing
- Check documents for compliance with major regulations
- User-friendly Streamlit interface

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
   
   git clone <repository-url>
   cd Compliance_Agent

2. Install dependencies:
   
   pip install -r requirements.txt

3. Set up your OpenAI API key:
   
   Option 1: Set as an environment variable
   
   export OPENAI_API_KEY="your-api-key-here"
   
   Option 2: Create a .env file
   
   echo "OPENAI_API_KEY=your-api-key-here" > .env

4. Run the application:
   
   streamlit run app.py

5. Open your browser and go to http://localhost:8501

## Usage Guide

1. Upload one or more documents (PDF, TXT, XLSX, CSV, DOCX)
2. Configure summarization settings in the sidebar (model, summary length, storage type)
3. Click Summarize to generate summaries or key takeaways
4. Save summaries to your chosen storage format
5. Use the compliance checker to analyze documents for regulatory violations
6. Search and manage your document library in the knowledge base

## Architecture

- app.py: Main Streamlit application
- document_processor.py: Handles text extraction from various formats
- llm_summarizer.py: Integrates with OpenAI API for summarization
- storage_manager.py: Manages data storage (JSON, CSV, SQLite)
- compliance_agent.py: Compliance checking logic
- requirements.txt: Python dependencies

## Configuration

- Set your OpenAI API key in the .env file or as an environment variable
- Adjust supported file types in document_processor.py if needed
- Customize compliance rules in compliance_agent.py

## Security and Privacy

- All document processing is performed locally
- OpenAI API calls are made securely over HTTPS
- Summaries and data are stored locally on your machine
- No data is shared with third parties except for OpenAI API calls

## Troubleshooting

- Ensure your OpenAI API key is valid and has sufficient credits
- Check that all dependencies are installed
- For file upload issues, verify the file format and size
- For compliance errors, review the compliance_agent.py logic
