# AI Agent Architecture Document

## 1. Overview

This document outlines the architecture of the AI Research Assistant, a prototype designed to automate the initial steps of a literature review. The system is built on a **Planner + Executor** multi-agent design pattern. This pattern separates the high-level task of "planning" from the low-level task of "execution," creating a modular and extensible system.

The agent's core responsibility is to take a user-defined research topic, find relevant academic papers, and summarize them using a custom fine-tuned language model.

## 2. System Components

The agent is composed of three primary components: the Planner Agent, the Executor Agent, and a set of Tools.

### 2.1. Planner Agent

-   **Responsibility:** To decompose the user's high-level request (e.g., "find papers on quantum computing") into a structured, machine-readable plan.
-   **Current Implementation:** In this prototype, the Planner is a **hard-coded function** that generates a static, three-step plan: (1) search, (2) summarize, (3) synthesize.
-   **Reasoning for Choice:** For a rapid prototype, a hard-coded planner is sufficient to build and test the complete execution workflow. It allows development to focus on the more complex parts of the system, such as tool use and model integration. A future iteration would replace this with an LLM call for dynamic, intelligent planning.

### 2.2. Executor Agent

-   **Responsibility:** To receive the plan from the Planner and execute each step in sequence.
-   **Implementation:** The Executor iterates through the plan's steps. For each step, it identifies the required tool (e.g., `search_papers`), gathers the necessary inputs (e.g., the user's query), and invokes the tool. It also manages the flow of data between steps, passing the output of one task as the input to the next.

### 2.3. Tools

Tools are specialized modules that the Executor Agent uses to interact with the outside world or perform complex computations.

-   **`PaperSearchTool`:**
    -   **Purpose:** To retrieve academic literature from external sources.
    -   **Integration:** It uses the official `arxiv` Python library to connect to the arXiv API.
    -   **Reasoning for Choice:** The arXiv API was chosen over others because it is fast, reliable, and does not require an API key for immediate use, making it ideal for rapid development.

-   **`SummarizerTool`:**
    -   **Purpose:** To generate a concise, single-sentence summary of a given academic abstract.
    -   **Integration:** This tool loads the `TinyLlama-1.1B` base model and applies a custom-trained LoRA adapter from the local `./fine_tuned_summarizer` directory.
    -   **Reasoning for Choice:** This is the core of the project's mandatory requirement. By encapsulating the fine-tuned model in a tool, we allow the Executor to treat summarization as just another capability, making the system clean and modular.

## 3. Interaction Flow

1.  **User Input:** The user provides a research topic via the Command Line Interface (CLI).
2.  **Planning:** The `PlannerAgent` receives the topic and generates a static JSON plan.
3.  **Execution:** The `ExecutorAgent` receives the plan.
    -   **Step 1:** It executes the `search_papers` task by calling the `PaperSearchTool`, which returns a list of papers.
    -   **Step 2:** It executes the `summarize_papers` task. It takes the abstracts from the previous step and passes them to the `SummarizerTool`, which returns a list of summaries.
4.  **Output:** The final list of papers, now enriched with their custom summaries, is formatted and displayed to the user in the CLI.