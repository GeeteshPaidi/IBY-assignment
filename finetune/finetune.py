# finetune.py (CPU-RELIABLE VERSION)

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)

def finetune_summarizer_cpu():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    print(f"Loading base model: {model_name}...")

    # --- KEY CHANGE: REMOVED BITSANDBYTES ---
    # We are now loading the model in its standard precision because
    # bitsandbytes is not reliable on CPU.
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    print("Loading dataset from local file: local_arxiv.jsonl...")
    dataset = load_dataset('json', data_files='local_arxiv.jsonl', split='train')

    def format_prompt(example):
        return f"### Instruction: Summarize the following academic abstract into a single, concise sentence.\n### Abstract:\n{example['abstract']}\n### Summary:\n{example['summary']}"

    data = dataset.map(lambda example: {"text": format_prompt(example)})
    print(f"Dataset prepared. Using {len(data)} examples for fine-tuning.")

    # We still use LoRA, as it reduces the number of parameters to train,
    # which is very helpful even on a CPU.
    lora_config = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
    model = get_peft_model(model, lora_config)

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=2e-4,
        num_train_epochs=3,
        logging_steps=2,
        # We remove fp16=True as it is also a GPU-specific optimization
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        train_dataset=data,
        args=training_args,
        data_collator=lambda data: {
            'input_ids': (ids := torch.stack([tokenizer(item['text'], return_tensors="pt", padding="max_length", max_length=512, truncation=True).input_ids.squeeze(0) for item in data])),
            'labels': ids.clone()
        },
    )

    print("Starting fine-tuning...")
    trainer.train()
    print("Fine-tuning completed!")

    adapter_path = "./fine_tuned_summarizer"
    model.save_pretrained(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    print(f"Fine-tuned model adapter saved to {adapter_path}")

if __name__ == "__main__":
    finetune_summarizer_cpu()