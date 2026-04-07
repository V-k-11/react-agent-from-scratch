## ReAct Agent from Scratch

A minimal, framework-free ReAct (Reasoning + Acting) agent built in pure Python.
No LangChain. No LlamaIndex. Just raw loops, prompts, and tools.

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/react-agent-from-scratch
cd react-agent-from-scratch
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # Add your Groq API key
streamlit run app.py
```

## API Keys
| Service | Key Required | Where to Get |
|---|---|---|
| Groq (LLM) |  Free | [console.groq.com](https://console.groq.com/keys) |
| Open-Meteo (Weather) |  None | Auto |
| DuckDuckGo (Search) |  None | Auto |
| Wikipedia |  None | Auto |

