# AI Research Agent

A Streamlit app that turns a folder of research documents into a structured, source-cited company brief using the Groq LLM API.

## How it works

1. Drop your research files (`.md`, `.txt`, or `.pdf`) into the `research_pack/` folder, or upload one or more documents directly in the UI.
2. Enter a company ticker in the UI and click **Generate brief**.
3. The agent reads the uploaded documents (when provided), otherwise the local research pack, sends them to the LLM with a strict system prompt, and returns a one-page Markdown brief with sections: Snapshot, Bull case, Bear case, Open questions, and Sources.
4. Download the brief as a `.md` file. Each generated response is also saved unchanged in `generated_briefs/`.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=<your_groq_api_key>
GROQ_MODEL=llama-3.3-70b-versatile   # optional, this is the default
```

## Run

```bash
streamlit run app.py
```

## Project structure

```
research_pack/      # Put your source documents here
generated_briefs/   # Exact generated briefs saved by ticker
app.py              # Streamlit UI
research_agent.py   # Document loader + Groq API call
system_prompt.md    # LLM instructions
```

## Notes

- The agent only uses the documents you provide — it does not browse the internet.
- Total research text is capped at 100,000 characters per request.
- The LLM is instructed to flag conflicting figures, treat promotional content skeptically, and never give personalized investment advice.
