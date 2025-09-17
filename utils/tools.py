import os
import warnings
import logging as py_logging
import arxiv
from transformers.utils import logging as hf_logging

# Quiet third-party logs/warnings
os.environ["BITSANDBYTES_NOWELCOME"] = "1"
hf_logging.set_verbosity_error()
py_logging.getLogger("bitsandbytes").setLevel(py_logging.ERROR)
warnings.filterwarnings("ignore")

class PaperSearchTool:
    def search_papers(self, query: str, max_results: int = 10) -> list[dict]:
        if not query or not query.strip():
            return []
        if max_results <= 0:
            return []
        try:
            search = arxiv.Search(
                query=query.strip(),
                max_results=min(max_results, 100),  # Limit to 100 to prevent excessive requests
                sort_by=arxiv.SortCriterion.Relevance
            )

            paper_list = []
            for result in search.results():
                authors = [author.name for author in result.authors]
                
                paper_list.append({
                    'paperId': result.entry_id,
                    'title': result.title,
                    'abstract': result.summary.replace('\n', ' ').strip(),
                    'authors': authors,
                    'published': result.published.isoformat() if result.published else None,
                    'url': result.entry_id
                })
            
            return paper_list

        except arxiv.ArxivError:
            return []
        except Exception:
            return []

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

class SummarizerTool:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load base model and apply fine-tuned LoRA adapter."""
        base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        adapter_path = "./fine_tuned_summarizer"

        # silence loading prints
        
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            trust_remote_code=True,
            torch_dtype=torch.float32
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            adapter_path,
            trust_remote_code=True
        )

        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model = self.model.merge_and_unload()
        
        # ready

    def summarize(self, abstracts: list[str]) -> list[str]:
        """Generate one summary per abstract."""
        summaries = []
        for abstract in abstracts:
            prompt = f"### Instruction: Summarize the following academic abstract into a single, concise sentence.\n### Abstract:\n{abstract}\n### Summary:\n"
            inputs = self.tokenizer(prompt, return_tensors="pt")
            generation_config = GenerationConfig(
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                top_p=0.95
            )
            outputs = self.model.generate(**inputs, generation_config=generation_config)
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            summary = full_output.split("### Summary:")[1].strip()
            summaries.append(summary)

        return summaries
        
# Example of how to use the tool (for testing)
if __name__ == '__main__':
    search_tool = PaperSearchTool()
    papers = search_tool.search_papers("quantum computing", max_results=5)
    
    if papers:
        print(f"\n--- Search Results ---")
        for i, paper in enumerate(papers, 1):
            print(f"{i}. {paper['title']}")
            print(f"   Abstract: {paper['abstract'][:150]}...")
        print("--------------------")