
# Multi-agent research team

A small LangGraph team that answers a question in four steps.

Built as a junior GenAI portfolio project.

## Flow

researcher -> writer -> critic -> revise

- Researcher collects facts
- Writer drafts an answer from those notes only
- Critic checks the draft for invented facts
- Revise writes the final answer using the critic notes

## Tech stack

- Python
- LangGraph
- Groq (qwen/qwen3.8-27b)

## How to run

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_key_here
GROQ_CHAT_MODEL=qwen/qwen3.8-27b

Then:

python ask.py

## What I learned

- Agents share one state object instead of calling each other directly
- The graph decides the order
- The same model name must exist on the current Groq account
- .env must stay out of Git
