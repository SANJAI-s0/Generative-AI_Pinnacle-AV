# Generative AI Pinnacle AV

This repository contains multiple standalone AI, ML, automation, and generative AI projects organized as separate folders under the root. Each project has its own `README.md`, dependencies, and workflow.

## Repository Overview

The workspace includes projects such as:

- `agentic-expense-tracker`
- `BPE`
- `Conversational_AI`
- `CPCB`
- `crewai-code-debugger`
- `crewai-role-based-ai-interviewer`
- `Customer_Subscription-Based`
- `FineTuning`
- `langgraph-research-agent`
- `Logistics_Optimization_Analysis-Crew_AI`
- `ML_Model`
- `n8n`
- `NYC_Taxi_Prediction`
- `ReAct`
- `Sentiment_Analysis`
- `Travel_Assistant_AI`

Each folder is intended to be treated as an independent project and can be pushed separately to GitHub.

## Folder Structure

```
AV_Projects/
├── agentic-expense-tracker/
├── BPE/
├── Conversational_AI/
├── CPCB/
├── crewai-code-debugger/
├── crewai-role-based-ai-interviewer/
├── Customer_Subscription-Based/
├── FineTuning/
├── langgraph-research-agent/
├── Logistics_Optimization_Analysis-Crew_AI/
├── ML_Model/
├── n8n/
├── NYC_Taxi_Prediction/
├── ReAct/
├── Sentiment_Analysis/
├── Travel_Assistant_AI/
├── README.md
└── LICENSE
```

## Prerequisites

- Git installed and configured
- Python 3.10+ installed
- Optional virtual environment for Python projects
- GitHub remote configured as `origin`

## Initial Setup

1. Clone the repository
2. Open the repo root
3. Activate the virtual environment if used
4. Install dependencies for each project as needed

Example:

```powershell
cd Z:\AV_Projects
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned)
& .venv\Scripts\Activate.ps1
```

## Project Workflow

### 1. Read the project README

Before running or pushing a project, open its own `README.md` inside the project folder to understand setup, dependencies, and execution instructions.

### 2. Check status

```powershell
git status
```

### 3. Add and commit a single project

Each project can be committed separately. Use the folder name as the staging target.

Example:

```powershell
git add agentic-expense-tracker
git commit -m "🧾 Agentic Expense Tracker"
git push origin HEAD
```

### 4. Push project-wise

Recommended workflow for this repository:

```powershell
# Example: push one project at a time
git add agentic-expense-tracker
git commit -m "🧾 Agentic Expense Tracker"
git push origin HEAD

git add BPE
git commit -m "WikiText-2 BPE Tokenizer"
git push origin HEAD

git add Conversational_AI
git commit -m "Conversational AI — Clothing Store Competitor Analyzer"
git push origin HEAD
```

You can repeat this process for every project folder.

## Commit Message Guidelines

Use clear and descriptive commit messages. A good pattern is:

- Keep the project title from its README
- Use emojis only if consistent with the project style
- Keep the message short and meaningful

Examples:

- `🧾 Agentic Expense Tracker`
- `🤖 QLoRA BERT Text Classification`
- `🚕 NYC Taxi Trip Duration Prediction`

## Running Projects

Each project contains its own execution instructions. Common patterns include:

- Python scripts executed via `python script.py`
- Jupyter notebooks opened in VS Code or Jupyter
- Requirements installation via `pip install -r requirements.txt`

Always run project setup from inside that project folder unless the README explicitly directs otherwise.

## Git Push Notes

- Commit from the root repository only.
- Stage the project folder name, not a single file.
- Push one project at a time to keep history cleaner.
- If a project has no changed files, skip it.

## Suggested Automation Script

You can run project-wise commits using a PowerShell loop, for example:

```powershell
$projects = @(
    'agentic-expense-tracker',
    'BPE',
    'Conversational_AI',
    'CPCB',
    'crewai-code-debugger',
    'crewai-role-based-ai-interviewer',
    'Customer_Subscription-Based',
    'FineTuning',
    'langgraph-research-agent',
    'Logistics_Optimization_Analysis-Crew_AI',
    'ML_Model',
    'n8n',
    'NYC_Taxi_Prediction',
    'ReAct',
    'Sentiment_Analysis',
    'Travel_Assistant_AI'
)

foreach ($project in $projects) {
    git add $project
    git commit -m "Update $project"
    git push origin HEAD
}
```

Adjust commit messages per project if needed.

## Repository Maintenance

- Review branch status before pushing
- Keep `requirements.txt` updated in each project
- Maintain the project-level README files
- Avoid mixing unrelated changes into one commit when pushing project-wise

## Support

If any project needs environment setup help, open its project folder and read its local `README.md` first. The root README is intended as the repository-level guide only.
