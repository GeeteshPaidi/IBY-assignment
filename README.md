# AI Research Assistant

Name: Paidi Geetesh Chandra   
University: Indian Institute of Technology Kharagpur   
Department: Metallurgical and Materials Engineering   

## Overview

Lightweight CLI that searches arXiv for papers on a topic and generates **summaries** using a fine-tuned TinyLlama model (LoRA). Output is minimal: title and summary only.

## Project Structure

```
├── main.py                    # CLI entrypoint
├── utils/
│   ├── agents.py             # Planner and Executor
│   └── tools.py              # arXiv search + summarizer tools
├── finetune/
│   ├── finetune.py           # Fine-tuning utilities
│   └── local_arxiv.jsonl     # Local data/cache
└── README.md
```

## Setup

You can use **Poetry** (recommended) or **pip**.

### Poetry

1. Install Poetry and run:
   ```bash
   poetry install
   ```
2. Activate the environment:
   ```bash
   poetry shell
   ```

### Pip

1. Create/activate a virtual environment (optional) and run:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
poetry run python main.py
```
or
```bash
python main.py
```

## Usage

1. **Enter a topic**, or type `exit` to quit
2. **Enter number of papers** (1–15). Press Enter for default 5
3. **View results**: You'll see compact results with just title and summary
4. **Continue or exit**: When prompted, enter `n` to stop, or `y` to search another topic

## Important Notes

- **Clean output**: Logs and library warnings are suppressed to keep the output clean
- **Model requirement**: Summarizer expects a LoRA adapter at `./fine_tuned_summarizer`. If missing, train via `finetune/finetune.py` or adapt `SummarizerTool` to a different model

## Troubleshooting

- **Missing dependencies**: If you see `ModuleNotFoundError: arxiv`, install it (Poetry will) or `pip install arxiv`
- **Slow first run**: Large model downloads can be slow on first run; subsequent runs are cached


