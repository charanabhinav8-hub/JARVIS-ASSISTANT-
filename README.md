# JARVIS - Personal Computer Assistant

A sophisticated AI-powered personal assistant for your computer, inspired by JARVIS from Iron Man. Control your computer entirely through natural language commands with voice input/output, task automation, and intelligent decision-making.

## Features

- 🎙️ **Voice Input/Output** - Speak commands naturally, receive audio responses
- 🧠 **Natural Language Understanding** - Advanced NLU using spaCy and Gemini API
- ⚙️ **Task Automation** - File management, scheduling, system control
- 🔗 **Application Integration** - Control multiple applications seamlessly
- 🌐 **Web Search & Information** - Real-time web search and data retrieval
- 📅 **Calendar & Email** - Manage appointments and emails
- 💻 **Full Computer Control** - Execute system commands and scripts
- 🔐 **Security** - Encrypted API keys and secure task execution

## Tech Stack

- **Language**: Python 3.9+
- **Voice**: Google Text-to-Speech (gTTS) & SpeechRecognition
- **NLP**: spaCy, NLTK
- **AI**: Google Gemini API
- **Automation**: PyAutoGUI, Schedule, Pyperclip
- **System**: OS, Subprocess, Platform utilities

## Installation

```bash
git clone https://github.com/charanabhinav8-hub/JARVIS-ASSISTANT-.git
cd JARVIS-ASSISTANT-
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory
2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Configure preferences in `config/config.json`

## Usage

```bash
python main.py
```

Say "Hey JARVIS" followed by your command.

## Project Structure

```
JARVIS-ASSISTANT-/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                    # API keys (not in git)
├── config/
│   ├── config.json        # Configuration settings
│   └── commands.json      # Custom commands
├── core/
│   ├── voice.py           # Voice I/O
│   ├── nlp.py             # NLP processing
│   ├── gemini.py          # Gemini API integration
│   └── task_executor.py   # Task execution
├── modules/
│   ├── file_manager.py    # File operations
│   ├── system_control.py  # System commands
│   ├── web_search.py      # Web search
│   └── app_control.py     # Application control
└── utils/
    ├── logger.py          # Logging
    └── helpers.py         # Utility functions
```

## Example Commands

- "Open chrome"
- "Search for Python tutorials"
- "Create a file named notes.txt"
- "Send an email to john@example.com"
- "Set a reminder for tomorrow at 2 PM"
- "Close all applications"
- "What's the weather today?"
- "Open my documents folder"

## Getting Started

1. **Get Gemini API Key**: https://aistudio.google.com/apikey
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Download spaCy Model**: `python -m spacy download en_core_web_sm`
4. **Configure .env**: Add your API key
5. **Run JARVIS**: `python main.py`

## Security Notes

- Keep your `.env` file private (it's in `.gitignore`)
- Never commit API keys to repository
- Review dangerous command settings before use
- Enable confirmation for system modifications

## License

MIT License
