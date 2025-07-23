# terzo-ai-coding
DYI AI Coding Assistant, codebase provided by Claude Sonnet

## Summary

Ain't nobody got time to pay $20 a month for an AI coding assistant.

### Problem

### Data

### Method

1. Clone Repository

    PS C:\Projects> git clone https://github.com/spycebot/terzo-ai-coding.git
    PS C:\Projects> cd terzo-ai-coding

1. Create Virtual Environment

    PS C:\Projects\terzo-ai-coding> C:\...\AppData\Local\Programs\Python\Python313\python.exe
    PS C:\Projects\terzo-ai-coding> .venv\scripts\activate

1. Install Dependencies

    (.venv) PS C:\Projects\terzo-ai-coding> pip install requests python-dotenv pyyaml flask fastapi uvicorn tree-sitter

1. Create directory structure and copy in files that Claude gave

### Model

Project Structure

ai-coding-assistant/
├── src/
│   ├── __init__.py
│   ├── assistant.py
│   ├── ollama_client.py
│   ├── code_parser.py
│   ├── context_manager.py
│   └── ui/
│       ├── cli.py
│       ├── web_interface.py
│       └── vscode_extension/
├── config/
│   └── config.yaml
├── requirements.txt
└── README.md

### Discussion