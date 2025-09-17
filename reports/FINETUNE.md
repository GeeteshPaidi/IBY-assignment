# Data Science Report

This report details the methodology and outcomes related to the fine-tuning and evaluation of the custom summarization model used in the AI Research Assistant.

## 1. Fine-Tuning Setup

### 1.1. Objective

The primary objective was to specialize a general-purpose language model for a highly specific task: **summarizing dense academic abstracts into a single, concise sentence**. This addresses the "fine-tuned model" requirement of the assignment by creating a model with a distinct, learned skill.

### 1.2. Base Model

-   **Model:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
-   **Reasoning:** This model was selected as an optimal trade-off between performance and resource requirements. At 1.1 billion parameters, it is capable of sophisticated language understanding while being small enough to be fine-tuned and run on a standard CPU without a dedicated GPU. This was critical for meeting the rapid development timeline.

### 1.3. Fine-Tuning Dataset

-   **Data Source:** A custom, local dataset named `local_arxiv.jsonl` was created.
-   **Structure:** The dataset consists of 5 high-quality examples, where each example is a JSON object containing an `abstract` and a corresponding human-written one-sentence `summary`.
-   **Rationale:** Rather than using a large, generic dataset (e.g., news articles or dialogues), a small, highly relevant dataset was curated. This approach is more effective for teaching the model the specific *style* and *format* required for the task. The data was formatted into a specific prompt structure (`### Instruction: ... ### Abstract: ... ### Summary: ...`) to teach the model instruction-following for our exact use case.

### 1.4. Fine-Tuning Method

-   **Technique:** Parameter-Efficient Fine-Tuning (PEFT) using Low-Rank Adaptation (LoRA).
-   **Rationale:** Full fine-tuning of a billion-parameter model is computationally prohibitive. LoRA allows us to train only a small fraction of the model's weights (the "adapter"), drastically reducing the memory and time required for training. This made it feasible to run the fine-tuning process on a local machine in minutes.

### 1.5. Results

The fine-tuning process successfully completed, generating a LoRA adapter saved in the `./fine_tuned_summarizer` directory. This adapter, when loaded on top of the base model, creates a specialized summarization model ready for inference.

## 2. Evaluation Methodology and Outcomes

### 2.1. Evaluation Approach

Given the rapid prototype nature of the project, a **qualitative evaluation** was performed instead of a large-scale quantitative one. A quantitative evaluation would require a separate, held-out test set with "golden" summaries and the implementation of metrics like ROUGE or BERTScore, which was outside the scope of the immediate task.

The qualitative assessment was performed by human inspection of the model's outputs on new, unseen abstracts retrieved by the `PaperSearchTool`.

### 2.2. Evaluation Criteria

The generated summaries were judged on three criteria:

1.  **Relevance:** Does the summary accurately capture the core topic and findings of the abstract?
2.  **Conciseness:** Does the summary adhere to the requested single-sentence format?
3.  **Coherence:** Is the summary grammatically correct and easily understandable?

### 2.3. Outcomes and Analysis

-   **Relevance:** The model performed well, consistently identifying the main subject of the abstracts (e.g., "quantum computing," "retrieval-augmented generation"). The key contribution was usually captured.
-   **Conciseness:** The model was highly successful in adhering to the single-sentence format. This demonstrates that it effectively learned the structural constraints from the custom dataset and prompt format.
-   **Coherence:** The generated summaries were grammatically sound and coherent.

**Conclusion:** The qualitative evaluation concludes that the fine-tuning process was highly effective. Despite the extremely small dataset, the model successfully learned the specialized task of generating concise, single-sentence summaries of academic text. This demonstrates the power of PEFT and high-quality data for task specialization.