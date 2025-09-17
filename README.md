AI Research Assistant

Overview

Lightweight CLI that searches arXiv for papers on a topic and generates one‑line summaries using a fine‑tuned TinyLlama model (LoRA). Output is minimal: title and summary only.

Project layout

- main.py: CLI entrypoint
- utils/agents.py: Planner and Executor
- utils/tools.py: arXiv search + summarizer tools
- finetune/finetune.py: optional fine‑tuning utilities
- finetune/local_arxiv.jsonl: optional local data/cache

Setup

You can use Poetry (recommended) or pip.

Poetry

1) Install Poetry and run:
   poetry install
2) Activate the env:
   poetry shell

Pip

1) Create/activate a venv (optional) and run:
   pip install -r requirements.txt

Run

poetry run python main.py
or
python main.py

Usage

1) Enter a topic, or type exit to quit.
2) Enter number of papers (1–15). Press Enter for default 5.
3) You’ll see compact results: just title and summary.
4) When prompted, enter n to stop, or y to search another topic.

Notes

- Logs and library warnings are suppressed to keep the output clean.
- Summarizer expects a LoRA adapter at ./fine_tuned_summarizer. If missing, train via finetune/finetune.py or adapt SummarizerTool to a different model.

Troubleshooting

- If you see ModuleNotFoundError: arxiv, install it (Poetry will) or pip install arxiv.
- Large model downloads can be slow on first run; subsequent runs are cached.


