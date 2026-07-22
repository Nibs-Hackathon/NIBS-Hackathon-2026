# NIBS-Hackathon-2026
Hackathon 2026

## Gemini setup

The AI Assistant uses the existing RAG-backed KnowledgeAgent, which requires a
Gemini API key. Create a local configuration file before using the assistant:

```powershell
Copy-Item .env.example .env
```

Then replace `YOUR_GEMINI_API_KEY_HERE` in `.env` with a real Gemini API key.
The `.env` file is ignored by Git and must not be committed.

The application loads the repository-root `.env` automatically and supports
these environment variable names: `GEMINI_API_KEY_1` (preferred),
`GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_KEY_1`.

The default production model is `gemini-3.6-flash`. Set `GEMINI_MODEL` in
`.env` only when you need to select another model available to your Gemini API
project.
