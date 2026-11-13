# Prompt Engineering & LLM Evaluation Harness

An enterprise-grade, asynchronous testing and evaluation framework designed to benchmark, evaluate, and compare modern Large Language Models (LLMs) across standard prompt engineering patterns.

[Source repo information](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/01-prompt-engineering)

---

This repository provides an automated test harness to evaluate how different foundation models respond to structured prompt engineering techniques. Rather than relying on static or qualitative impressions, the framework systematically quantifies model performance across four key axes:

1. **Instruction Following & Constraint Compliance:** Enforces format validity (e.g. strict JSON, lists), length budgets, and keyword requirements.
2. **Quality & Composite Scoring:** Evaluates pattern alignment against deterministic criteria defined per pattern.
3. **Token Efficiency:** Tracks prompt, completion, and total token usage across providers.
4. **End-to-End Latency:** Measures wall-clock execution time for cross-provider performance analysis.

---

## Architecture 

The codebase follows a decoupled, modular architecture designed for high throughput and extensibility:

- **`src/prompt_code/prompt_patterns.py`**: Catalog of parameterized prompt engineering patterns (Persona, Few-Shot, Chain-of-Thought, Critique, Guardrails, Boundary, Audience Adaptation, Decomposition, Meta-Prompting).
- **`src/prompt_code/prompt_builder.py`**: Template rendering engine that hydrates patterns with task-specific variables, metadata, and role assignments.
- **`src/prompt_code/harness.py`**: Asynchronous testing harness built on LangChain's universal abstractions (`init_chat_model`, `ainvoke`, `asyncio.gather`). Dispatches concurrent requests across providers without cross-model blocking.
- **`src/score/model_comparison.py`**: Evaluation engine that computes composite compliance scores based on required keywords, forbidden phrases, word count limits, and format integrity.
- **`src/tests/test_prompt.py`**: Automated test suite executing real LLM evaluations against curated scenarios within a unified event loop.

---

## Results: GPT-6 Luna vs. Claude Haiku 5.5

The suite was executed asynchronously across **10 distinct prompt patterns**, benchmarking **GPT-6 Luna** against **Claude Haiku 5.5** under matching runtime constraints.

### Aggregate Rankings

```text
======================================================================
  SUMMARY: MODEL RANKINGS ACROSS ALL TESTS
======================================================================
  gpt-6-luna: 10 wins out of 10 tests
```

### Detailed Evaluation Output

```text
======================================================================
  PROMPT ENGINEERING TEST SUITE
======================================================================

============================================================
  Test: Persona: Technical Writer
  Pattern: persona
============================================================

  System: You are an AI assistant using the Persona Pattern...
  User prompt: You are a senior technical writer at Stripe with 10 years of API documentation experience.
Your communication style is p...
  Temperature: 0.7

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      240  6279.73ms
  claude-haiku-5-5             0.667      779  3665.67ms

============================================================
  Test: Few-Shot: Sentiment Analysis
  Pattern: few_shot
============================================================

  System: You are an AI assistant using the Few-Shot Pattern...
  User prompt: Here are examples of the expected input/output format:

Input: "The food was amazing but service was slow"
Output: {"sen...
  Temperature: 0.0

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      253  2621.52ms
  claude-haiku-5-5             1.000      368  1502.88ms

============================================================
  Test: Chain-of-Thought: Math Problem
  Pattern: chain_of_thought
============================================================

  System: You are an AI assistant using the Chain-of-Thought Pattern...
  User prompt: Think through this step by step.

Problem: A store offers 20% off all items. An item originally costs $85. There is also...
  Temperature: 0.3

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      357  3757.31ms
  claude-haiku-5-5             1.000      820  3328.42ms

============================================================
  Test: Template Fill: Resume Extraction
  Pattern: template_fill
============================================================

  System: You are an AI assistant using the Template Fill Pattern...
  User prompt: Extract information from the following text and fill in the template.

Text: John Smith is a software engineer at Google...
  Temperature: 0.0

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      193  1979.09ms
  claude-haiku-5-5             1.000      250   902.53ms

============================================================
  Test: Guardrail: Scoped Assistant
  Pattern: guardrail
============================================================

  System: You are an AI assistant using the Guardrail Pattern...
  User prompt: You are a Python programming tutor.

Rules:
- ONLY answer questions about Python programming
- If the question is outsid...
  Temperature: 0.3

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      243  2920.55ms
  claude-haiku-5-5             1.000      690  3695.59ms

============================================================
  Test: Critique: Concurrent Wallet Deduct
  Pattern: critique
============================================================

  System: You are an AI assistant using the Critique Pattern...
  User prompt: Task: Design a Python function to process and deduct credits from a user's wallet in a database.The function must be saf...
  Temperature: 0.5

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000     1254 10874.25ms
  claude-haiku-5-5             0.667     2196  8856.33ms

============================================================
  Test: Boundary: CS2
  Pattern: boundary
============================================================

  System: You are an AI assistant using the Boundary Pattern...
  User prompt: You are an assistant that ONLY handles Counter Strike 2.

If the user's request is within scope, help them fully.
If the...
  Temperature: 0.0

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   0.833      121  3993.21ms
  claude-haiku-5-5             0.833      161   862.94ms

============================================================
  Test: Audience Adaptation: American Football
  Pattern: audience_adapt
============================================================

  System: You are an AI assistant using the Audience Adaptation Pattern...
  User prompt: Explain american football for the following audience: A 10-year-old (use analogies and clear examples), a college studen...
  Temperature: 0.5

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   0.500     2163 18507.25ms
  claude-haiku-5-5             0.375     1811 10301.04ms

============================================================
  Test: Decomposition: Anagram problem
  Pattern: decomposition
============================================================

  System: You are an AI assistant using the Decomposition Pattern...
  User prompt: Problem: Create a function in Python to determine if a word is an anagram or not

Break this into sub-problems:
1. List ...
  Temperature: 0.3

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   1.000      762  7332.38ms
  claude-haiku-5-5             1.000     2162  8870.69ms

============================================================
  Test: Meta-Prompt: SQL Query Generator
  Pattern: meta_prompt
============================================================

  System: You are an AI assistant using the Meta-Prompt Pattern...
  User prompt: Write a prompt for an LLM that will convert natural language user questions into safe, read-only SQL queries (PostgreSQL...
  Temperature: 0.7

  Model                        Score   Tokens    Latency
  -------------------------------------------------------
  gpt-6-luna                   0.667     2157 18961.83ms
  claude-haiku-5-5             0.667     2227  10550.8ms
```

---

## Key Performance Insights

- **Instruction & Constraint Adherence:** **GPT-6 Luna** achieved a perfect composite score (`1.000`) across 7 out of 10 patterns, demonstrating exceptional fidelity to negative constraints and keyword requirements.
- **Latency vs. Reasoning Depth:** **Claude Haiku 5.5** exhibited consistently faster initial response times on lightweight tasks (e.g. `902ms` vs `1979ms` in Template Fill), whereas GPT-6 Luna traded additional latency for higher constraint strictness and conciseness on complex reasoning patterns (e.g. Critique and Persona).
- **Token Efficiency:** Across reasoning and critique patterns, Claude Haiku tended to produce more verbose outputs (e.g. `2,196` tokens vs `1,254` tokens in Critique), impacting total execution budget.

---

## Getting Started

### 1. Requirements & Setup

Install dependencies using `uv` or `pip`:

```bash
uv sync
```

### 2. Environment Variables

Create a `.env` file in the project root containing your API keys:

```env
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="AIzaSy..."
```

### 3. Running the Test Suite

Execute the asynchronous benchmark suite via `uv`:

```bash
uv run src/main.py
```

### 4. Custom settings
You can test any prompt format/pattern you desire as long as you declare the `criteria` as in the `TEST_SUITE` and then modify the score function to get the score on what you need to evaluate it.
