class PlannerAgent:
    def create_plan(self, research_topic: str, max_results: int = 5) -> dict:
        return {
            "steps": [
                {
                    "task_id": 1,
                    "task": "search_papers",
                    "query": research_topic,
                    "max_results": max_results,
                },
                {
                    "task_id": 2,
                    "task": "summarize_papers",
                },
            ]
        }

class ExecutorAgent:
    def __init__(self, tools: dict):
        self.tools = tools

    def execute_plan(self, plan: dict) -> dict:
        task_outputs = {}

        for step in plan.get("steps", []):
            task_id = step["task_id"]
            task_name = step["task"]

            if task_name not in self.tools:
                task_outputs[task_id] = None
                continue

            tool_to_run = self.tools[task_name]

            if task_name == "search_papers":
                query = step.get("query", "")
                max_results = step.get("max_results", 5)
                task_outputs[task_id] = tool_to_run.search_papers(query, max_results)

            elif task_name == "summarize_papers":
                papers = task_outputs.get(1, [])
                if not papers:
                    task_outputs[task_id] = []
                    continue
                abstracts = [p.get("abstract", "") for p in papers]
                summaries = tool_to_run.summarize(abstracts)
                for i, paper in enumerate(papers):
                    paper["summary"] = summaries[i] if i < len(summaries) else ""
                task_outputs[task_id] = papers

            else:
                task_outputs[task_id] = None

        return task_outputs