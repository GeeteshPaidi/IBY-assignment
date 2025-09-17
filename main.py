from utils.agents import PlannerAgent, ExecutorAgent
from utils.tools import PaperSearchTool, SummarizerTool

def _ask_for_paper_count() -> int:
    while True:
        raw = input("Number of papers (1-15, default 5): ").strip()
        if raw == "":
            return 5
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= 15:
                return n
        print("Please enter an integer between 1 and 15.")

def main():
    search_tool = PaperSearchTool()
    summarizer_tool = SummarizerTool()

    available_tools = {
        "search_papers": search_tool,
        "summarize_papers": summarizer_tool,
    }

    planner = PlannerAgent()
    executor = ExecutorAgent(tools=available_tools)

    print("\nAI Research Assistant")
    print("Type 'exit' anytime to quit.")

    while True:
        research_topic = input("\nTopic: ").strip()
        if research_topic.lower() == "exit":
            print("Bye!")
            break

        max_results = _ask_for_paper_count()
        plan = planner.create_plan(research_topic, max_results=max_results)
        results = executor.execute_plan(plan)

        summarized_papers = results.get(2, [])
        if summarized_papers:
            print(f"\nResults for: {research_topic}")
            for i, paper in enumerate(summarized_papers, start=1):
                print(f"{i}. {paper.get('title','')}")
                print(f"   {paper.get('summary','')}")
        else:
            print("No results.")

        again = input("\nSearch another topic? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Bye!")
            break

if __name__ == "__main__":
    main()