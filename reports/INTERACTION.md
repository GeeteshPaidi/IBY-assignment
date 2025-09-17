Development Interaction Log   
This log captures key interactions and prompts used while building the AI agent.

**1. Project Setup**
- My prompt:
  I want to use Poetry so dependencies can be managed and I can learn it as well. Can we learn and do it on the go?
- Context: I ran into a complex dependency error with PyTorch on Windows after initializing the project. I shared the error message and asked:
- My prompt:
  Should I re-initialize Poetry? Or what should I do?
- Outcome: The assistant guided me to add a custom source to my pyproject.toml file to solve the dependency conflict, which worked.

**2. API Integration**
- Context: The script for fetching papers was hanging without any output.
- My prompt:
  I am stuck on this for a long time; it is not giving any result. What should I do? Is there any issue in the code that I need to fix, or something like an API key to add so that I can get results?
- Context: After learning the API key would take too long, I explained my time constraint.
- My prompt:
  Because I received an email saying I will get the key in 2 weeks, I need to get this done in 2 hours.
- Outcome: We switched from the Semantic Scholar API to the arXiv API, which immediately solved the issue as it does not require an API key.

**3. Fine-Tuning the Model**
- Context: After an initial attempt with a generic dataset, I felt it was not relevant enough for the project's goal.
- My prompt:
  Our local dataset does not look very useful. Can it be better—something that looks good and relevant to our context?
- Outcome: The assistant helped me create a better, custom dataset using academic abstracts.
- Context: The training script was hanging without any progress. I let the assistant know.
- My prompt:
  It is still not running.
- Outcome: The assistant diagnosed the issue as a problem with the bitsandbytes library on a CPU. The final fix was to remove 4-bit quantization from the script, which allowed the training to complete.

**4. Final Submission**
- Context: Once the agent was fully functional, I needed to prepare the project for submission.
- My prompt: Cool, done. Now help me with the Git steps—what files to ignore, what files to upload, and so on.
- Outcome: The assistant provided a .gitignore file, and helped me create this interaction log.
