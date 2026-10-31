markdown
 Multi-Agent Research Team

An orchestrated multi-agent research and drafting system built with LangGraph, LangChain, and Groq. 

The system leverages live web search tool-calling, specialized role separation, structured Pydantic evaluations, and a conditional critique-and-revision feedback loop.

Built as a production-style junior GenAI portfolio project.

---

 Architecture & Workflow

text
       [User Query]
             │
             ▼
      [ Researcher ] ──► (Calls Web Search Tool to gather facts)
             │
             ▼
        [ Writer ] ◄────────────┐
             │                  │
             ▼                  │ (Needs Revision & Under Max Limit)
        [ Critic ] ─────────────┘
             │
             ▼ (Approved OR Max Revisions Reached)
        [ Finalize ]
             │
             ▼
       [ Final Answer ]


Agent Roles:

1. Researcher: Calls a web search tool (`DuckDuckGoSearchRun`) to retrieve verified, real-time facts instead of relying on stale training memory.
2. Writer: Synthesizes an answer grounded strictly in the research notes, incorporating feedback if looping from a critique.
3. Critic: Evaluates the draft against the research notes using **Pydantic structured output** (`approved: bool`, `feedback: str`). Checks for hallucinations, unsupported claims, and clarity.
4. Finalize: Promotes the approved draft to the final output once accepted or after reaching the revision cap.

---

Tech Stack

*Orchestration: LangGraph (StateGraph with conditional edges)
*Framework: LangChain (`langchain-core`, `langchain-community`)
*Validation: Pydantic v2 (Structured Outputs)
*Tools: DuckDuckGo Search
*LLM Engine: Groq API (`qwen/qwen3.8-27b` or compatible model)
*Environment: Python 3.11+, Windows PowerShell

---

Getting Started

1. Setup Virtual Environment

powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


2. Configure Environment Variables

Create a `.env` file in the project root:

env
GROQ_API_KEY=your_groq_api_key_here
GROQ_CHAT_MODEL=qwen/qwen3.8-27b

3. Run the CLI

powershell
python ask.py


---

## Key Engineering Takeaways

*Explicit State Machines Over Prompt Chaining:** Agents coordinate via an explicit, typed state dictionary (`TeamState`) rather than messy prompt-to-prompt handoffs.
*Controlled Orchestration Loops:** Replaced linear pipelines with conditional routing. Added a hard iteration guard (`MAX_REVISIONS = 2`) to eliminate runaway execution and unnecessary token consumption.
*Reliable Guardrails with Pydantic:** Using `.with_structured_output(CriticEvaluation)` ensures deterministic evaluation schemas rather than fragile regex or string matching on model responses.
*Grounded Verification:** The researcher acknowledges missing data instead of hallucinating facts when search returns partial information.
*Git & Secret Hygiene:** Enforced strict separation of configuration and secrets using `.env` and `.gitignore`.