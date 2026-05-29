# Generative AI Pinnacle AV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/SANJAI-s0/Generative-AI_Pinnacle-AV)](https://github.com/SANJAI-s0/Generative-AI_Pinnacle-AV/issues)
[![GitHub stars](https://img.shields.io/github/stars/SANJAI-s0/Generative-AI_Pinnacle-AV?style=social)](https://github.com/SANJAI-s0/Generative-AI_Pinnacle-AV)
[![GitHub last commit](https://img.shields.io/github/last-commit/SANJAI-s0/Generative-AI_Pinnacle-AV)](https://github.com/SANJAI-s0/Generative-AI_Pinnacle-AV/commits/main)

## Table of Contents

- [Repository Overview](#repository-overview)
- [Project Portfolio](#project-portfolio)
- [Repository Highlights](#repository-highlights)
- [Folder Structure](#folder-structure)
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Project Workflow](#project-workflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Running Projects](#running-projects)
- [Git Push Notes](#git-push-notes)
- [Suggested Automation Script](#suggested-automation-script)
- [Repository Maintenance](#repository-maintenance)
- [Support](#support)

## Repository Overview

This repository contains multiple standalone AI, ML, automation, and generative AI projects organized as separate folders under the root. Every project has its own local `README.md`, dependencies, and execution workflow.

The repository is designed for **project-wise development, experimentation, and GitHub pushes**, making it easy to track, commit, and manage each AI project independently.

## Project Portfolio

| Project | Problem | Solution | Description | Key Focus |
| --- | --- | --- | --- | --- |
| `agentic-expense-tracker` | Manual expense tracking is time-consuming and error-prone. | Agentic workflow for capturing and managing expenses. | Intelligent expense tracking assistant. | Automation, agent workflows |
| `BPE` | Text tokenization needs efficient subword handling. | Build and experiment with BPE tokenization. | WikiText-2 BPE tokenizer project. | NLP, tokenization |
| `Conversational_AI` | Need a conversational AI for competitor analysis. | Build conversational intelligence for retail analysis. | Clothing store competitor analyzer chatbot. | Conversational AI, analytics |
| `CPCB` | Water quality prediction needs robust AI modeling. | Use deep learning for water quality forecasting. | Environmental prediction project. | Deep learning, forecasting |
| `crewai-code-debugger` | AI code debugging requires structured analysis. | CrewAI-based debugging workflow. | Tool for debugging code with AI assistance. | Agentic debugging |
| `crewai-role-based-ai-interviewer` | Interview processes benefit from structured AI interviewer roles. | Role-based AI interviewer simulation. | AI-driven interview assistant. | Role-based AI, interviews |
| `Customer_Subscription-Based` | Subscription businesses need churn insights. | Predict churn and retention strategy. | Customer churn analysis and retention planning. | ML, retention |
| `FineTuning` | Need domain-specific fine-tuning workflows. | QLoRA BERT fine-tuning pipeline. | Text classification fine-tuning project. | Fine-tuning, NLP |
| `langgraph-research-agent` | Research summarization across topics is repetitive. | LangGraph-based research and summarization agent. | Multi-agent research system. | Agents, summarization |
| `Logistics_Optimization_Analysis-Crew_AI` | Logistics planning needs optimization. | CrewAI-driven optimization workflow. | Logistics optimization analysis. | Optimization, planning |
| `ML_Model` | Health classification prediction needs reliable modeling. | ML pipeline for health classification. | Insurance health classification model. | ML, healthcare |
| `n8n` | Automations need workflow orchestration. | n8n workflow automation templates. | AI-powered content creator workflow. | Automation, workflows |
| `NYC_Taxi_Prediction` | Taxi trip duration prediction helps demand forecasting. | Regression-based prediction models. | NYC taxi trip duration forecasting. | Predictive analytics |
| `ReAct` | Web research needs structured reasoning patterns. | ReAct-style research agent. | Web research agent using ReAct. | Reasoning, search |
| `Sentiment_Analysis` | Sentiment interpretation across models is complex. | Compare BERT, LSTM, GRU, and RNN performance. | Sentiment analysis benchmark project. | NLP, sentiment |
| `Travel_Assistant_AI` | Travelers need intelligent planning support. | AI travel assistant with recommendations. | Travel assistant project. | AI assistant, travel |

## Repository Highlights

- 16 independent AI/ML/automation projects under one repository.
- Each project can be committed and pushed separately for cleaner history.
- Root-level README, LICENSE, and `.gitignore` provide repository-wide conventions.
- Includes workflow examples for Git, Python, Jupyter, and automation-based projects.

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
