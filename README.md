# CodingWithR2D2

The goal of this project is to implement an AI agent capable of autonomously writing and verifying code to ensure it works as expected by giving it a prompt. Fork the repo and run it!

## Example Task / Prompt

An example task that the AI agent can solve:

- **Task**: Write a Python function that takes a list of numbers and returns the average of the numbers.
- **Process**: The AI agent writes the function in a Python file, verifies the correctness through testing, and outputs the working Python code.

---

## Overview

CodingWithR2D2 demonstrates how AI can generate functional Python code and validate its functionality autonomously. The agent:

1. Understands a given coding problem.
2. Generates a Python script that solves the problem.
3. Executes tests to verify correctness.
4. Outputs the final working code in a structured format.
5. Saves the prompt in log files.

## Setup

### Prerequisites

- **[Python 3.8+](https://www.python.org/downloads/)**: A widely-used programming language required to run the project.
- **[Llama 3.1:8b](https://ollama.com/)**: A powerful AI language model framework used in the project.

### Steps to run it:

1. Clone the repository:
   
   ```bash
   git clone https://github.com/SergioMM0/CodingWithR2D2.git

2. (Optional) Create and activate a virtual environment:
   
   ```bash
   python -m venv venv
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt

4. Run the agent with:

   ```bash
   python r2d2.py

5. Enjoy your AI coding partner! :)
