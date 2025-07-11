

import os
from typing import Dict, List

# OpenAI Configuration
OPENAI_CONFIG = {
    "default_model": "gpt-3.5-turbo",
    "available_models": [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview"
    ],
    "max_tokens": 4000,
    "temperature": 0.3,
    "top_p": 0.9,
    "timeout": 30, 
    "retry_attempts": 3
}

# Summary Configuration
SUMMARY_CONFIG = {
    "length_options": [
        "Short (100-200 words)",
        "Medium (200-400 words)", 
        "Long (400-600 words)"
    ],
    "word_limits": {
        "Short (100-200 words)": (100, 200),
        "Medium (200-400 words)": (200, 400),
        "Long (400-600 words)": (400, 600)
    },
    "max_input_length": 8000, 
    "tolerance_percentage": 20 
}

# File Processing Configuration
FILE_CONFIG = {
    "supported_formats": {
        "pdf": ["application/pdf"],
        "txt": ["text/plain"],
        "xlsx": [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel"
        ],
        "csv": ["text/csv"],
        "docx": [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]
    },
    "max_file_size_mb": 50,
    "encoding_fallback": "latin-1",
    "excel_max_rows": 20,  
    "csv_max_rows": 20
}

# Storage Configuration
STORAGE_CONFIG = {
    "default_storage": "sqlite",
    "storage_options": ["JSON", "CSV", "SQLite Database"],
    "database_file": "summaries.db",
    "json_file": "summaries.json",
    "csv_file": "summaries.csv",
    "backup_enabled": True,
    "backup_interval": 7,  # days
    "max_backups": 5
}

# UI Configuration
UI_CONFIG = {
    "page_title": "Document Summarizer",
    #"page_icon": "📄",
    "layout": "wide",
    "sidebar_state": "expanded",
    "theme": {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730"
    },
    "custom_css": """
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
            margin-bottom: 2rem;
        }
        .upload-section {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .summary-section {
            background-color: #e8f4fd;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .file-info {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
    """
}

# Cost Estimation Configuration
COST_CONFIG = {
    "models": {
        "gpt-3.5-turbo": {
            "input_cost_per_1k": 0.0015,
            "output_cost_per_1k": 0.002
        },
        "gpt-4": {
            "input_cost_per_1k": 0.03,
            "output_cost_per_1k": 0.06
        },
        "gpt-4-turbo-preview": {
            "input_cost_per_1k": 0.01,
            "output_cost_per_1k": 0.03
        }
    },
    "token_estimation_factor": 1.3,  # 1 word ≈ 1.3 tokens
    "default_output_tokens": 260  # ~200 words
}

# Error Handling Configuration
ERROR_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1, 
    "show_detailed_errors": True,
    "log_errors": True,
    "error_log_file": "error.log"
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "enable_caching": True,
    "cache_ttl": 3600, 
    "max_concurrent_requests": 5,
    "request_timeout": 30,
    "enable_progress_bars": True
}

# Security Configuration
SECURITY_CONFIG = {
    "api_key_validation": True,
    "file_type_validation": True,
    "file_size_validation": True,
    "sanitize_filenames": True,
    "allowed_file_extensions": [".pdf", ".txt", ".xlsx", ".csv", ".docx", ".doc"]
}

def get_config() -> Dict:
   
    return {
        "openai": OPENAI_CONFIG,
        "summary": SUMMARY_CONFIG,
        "file": FILE_CONFIG,
        "storage": STORAGE_CONFIG,
        "ui": UI_CONFIG,
        "cost": COST_CONFIG,
        "error": ERROR_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "security": SECURITY_CONFIG
    }

def get_env_config() -> Dict:
   
    config = {}
    
    
    if os.getenv("OPENAI_DEFAULT_MODEL"):
        config["openai_default_model"] = os.getenv("OPENAI_DEFAULT_MODEL")
    
    if os.getenv("OPENAI_TEMPERATURE"):
        config["openai_temperature"] = float(os.getenv("OPENAI_TEMPERATURE"))
    
    
    if os.getenv("DEFAULT_STORAGE"):
        config["default_storage"] = os.getenv("DEFAULT_STORAGE")
    
   
    if os.getenv("MAX_FILE_SIZE_MB"):
        config["max_file_size_mb"] = int(os.getenv("MAX_FILE_SIZE_MB"))
    
    return config

def validate_config() -> List[str]:
    
    errors = []
    
   
    if OPENAI_CONFIG["temperature"] < 0 or OPENAI_CONFIG["temperature"] > 2:
        errors.append("OpenAI temperature must be between 0 and 2")
    
    if OPENAI_CONFIG["max_tokens"] <= 0:
        errors.append("OpenAI max_tokens must be positive")
    
   
    for length, (min_words, max_words) in SUMMARY_CONFIG["word_limits"].items():
        if min_words >= max_words:
            errors.append(f"Word limits for {length} are invalid: min >= max")
    
    
    if FILE_CONFIG["max_file_size_mb"] <= 0:
        errors.append("Max file size must be positive")
  
    if STORAGE_CONFIG["backup_interval"] <= 0:
        errors.append("Backup interval must be positive")
    
    return errors

def print_config_summary():
    
    print(" Configuration Summary:")
    print(f"   • Default Model: {OPENAI_CONFIG['default_model']}")
    print(f"   • Default Storage: {STORAGE_CONFIG['default_storage']}")
    print(f"   • Max File Size: {FILE_CONFIG['max_file_size_mb']} MB")
    print(f"   • Supported Formats: {', '.join(FILE_CONFIG['supported_formats'].keys())}")
    print(f"   • Summary Lengths: {len(SUMMARY_CONFIG['length_options'])} options")
    print(f"   • UI Theme: {UI_CONFIG['theme']['primaryColor']}")

if __name__ == "__main__":
    
    errors = validate_config()
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("Configuration is valid")
        print_config_summary() 