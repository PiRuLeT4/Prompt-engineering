import asyncio
from prompt_code.prompt_builder import build_prompt
from prompt_code.harness import run_prompt_test_async
from score.model_comparison import  compare_models

TEST_SUITE = [
    {
        "name": "Persona: Technical Writer",
        "pattern": "persona",
        "variables": {
            "role": "a senior technical writer at Stripe",
            "experience": "10 years of API documentation experience",
            "style": "precise, concise, and example-driven",
            "priority": "clarity over comprehensiveness",
            "task": "Explain what an API rate limit is and why it exists.",
        },
        "criteria": {
            "max_words": 200,
            "required_keywords": ["rate limit", "API", "requests"],
            "forbidden_phrases": ["in conclusion", "it is important to note"],
        },
    },
    {
        "name": "Few-Shot: Sentiment Analysis",
        "pattern": "few_shot",
        "variables": {
            "examples": (
                'Input: "The food was amazing but service was slow"\n'
                'Output: {"sentiment": "mixed", "food": "positive", "service": "negative"}\n\n'
                'Input: "Terrible experience, never coming back"\n'
                'Output: {"sentiment": "negative", "food": null, "service": "negative"}'
            ),
            "input": "Great ambiance and the pasta was perfect, though a bit pricey",
        },
        "criteria": {
            "expected_format": "json",
            "required_keywords": ["sentiment"],
        },
    },
    {
        "name": "Chain-of-Thought: Math Problem",
        "pattern": "chain_of_thought",
        "variables": {
            "problem": "A store offers 20% off all items. An item originally costs $85. There is also a $10 coupon. Which saves more: applying the discount first then the coupon, or the coupon first then the discount?",
        },
        "criteria": {
            "required_keywords": ["discount", "coupon", "$"],
            "max_words": 300,
        },
    },
    {
        "name": "Template Fill: Resume Extraction",
        "pattern": "template_fill",
        "variables": {
            "text": "John Smith is a software engineer at Google with 5 years of experience. He graduated from MIT with a BS in Computer Science in 2019. He specializes in distributed systems and Go programming.",
            "template_structure": "Name: [full name]\nCompany: [current employer]\nYears of Experience: [number]\nEducation: [degree, school, year]\nSpecialties: [comma-separated list]",
        },
        "criteria": {
            "required_keywords": ["John Smith", "Google", "MIT"],
        },
    },
    {
        "name": "Guardrail: Scoped Assistant",
        "pattern": "guardrail",
        "variables": {
            "role": "Python programming tutor",
            "domain": "Python programming",
            "additional_rules": "Do not write complete solutions. Guide the student with hints.",
            "question": "How do I sort a list of dictionaries by a specific key?",
        },
        "criteria": {
            "required_keywords": ["sorted", "key", "lambda"],
            "forbidden_phrases": ["here is the complete solution"],
        },
    },
    {
        "name": "Critique: Concurrent Wallet Deduct",
        "pattern": "critique",
        "variables": {
            "task": (
                "Design a Python function to process and deduct credits from a user's wallet in a database."
                "The function must be safe against race conditions (double spending) when multiple requests arrive concurrently."
            ),
        },
        "criteria": {
            "required_keywords": ["step 1", "step 2", "transaction", "idempotency"],
            "forbidden_phrases": ["threading.lock", "global lock"],
            "max_words": 800,
        }, 
    },
    {
        "name": "Boundary: CS2",
        "pattern": "boundary",
        "variables": {
            "scope": "Counter Strike 2",
            "refusal_message": "I can't provide that information, I can only talk about CS2 the game.",
            "user_input": "What is the capital of France?"
        },
        "criteria": {
            "required_keywords": ["Counter Strike 2", "Cs2", "steam", "game"],
            "forbidden_phrases": ["Paris", "The capital of France is Paris"],
            "max_words": 200
        }
    },
    {
        "name": "Audience Adaptation: American Football",
        "pattern": "audience_adapt",
        "variables": {
            "concept": "american football",
            "audience": "A 10-year-old (use analogies and clear examples), a college student and a domain expert (assume full context, be precise)",
            "length": "400",
            "include": "One of the most famous sports",
            "exclude": "Agressive sport",
        },
        "criteria": {
            "required_keywords": ["sport", "football", "famous", "America"],
            "forbidden_phrases": ["Soccer", "Lionnel Messi"],
        }
    },
    {
        "name": "Decomposition: Anagram problem",
        "pattern": "decomposition",
        "variables": {
            "problem": "Create a function in Python to determine if a word is an anagram or not"
        },
        "criteria": {
            "expected_format": "numbered_list"
        }
    },
    {
        "name": "Meta-Prompt: SQL Query Generator",
        "pattern": "meta_prompt",
        "variables": {
            "objective": "convert natural language user questions into safe, read-only SQL queries (PostgreSQL)",
            "metric": "zero syntax errors and strict prevention of destructive operations (DROP, DELETE, UPDATE)",
            "model": "gpt-4o",
        },
        "criteria": {
            "required_keywords": [
                "role",
                "constraints",
                "example",
                "edge case",
                "SELECT",
            ],
            "forbidden_phrases": [
                "INSERT INTO",
                "DELETE FROM",
                "DROP TABLE",
            ],
            "max_words": 650,
        },
    },
]


async def run_test_suite_async():
    print("=" * 70)
    print("  PROMPT ENGINEERING TEST SUITE")
    print("=" * 70)

    all_results = []

    for test in TEST_SUITE:
        print(f"\n{'=' * 60}")
        print(f"  Test: {test['name']}")
        print(f"  Pattern: {test['pattern']}")
        print(f"{'=' * 60}")

        prompt = build_prompt(test["pattern"], test["variables"])
        print(f"\n  System: {prompt['system'][:80]}...")
        print(f"  User prompt: {prompt['user'][:120]}...")
        print(f"  Temperature: {prompt['temperature']}")

        results = await run_prompt_test_async(prompt)
        comparison, ranked = compare_models(results, test["criteria"])

        print(f"\n  {'Model':<25} {'Score':>8} {'Tokens':>8} {'Latency':>10}")
        print(f"  {'-'*55}")
        for model_name, data in ranked:
            score = data["scores"]["composite_score"]
            tokens = data["tokens"].get("total", 0)
            latency = data["latency_ms"]
            print(f"  {model_name:<25} {score:>8.3f} {tokens:>8} {latency:>8}ms")

            if data.get("error"):                          # 👈 muestra el error real
                print(f"      ↳ {data['error'][:150]}")

        all_results.append({
            "test": test["name"],
            "pattern": test["pattern"],
            "rankings": [(name, data["scores"]["composite_score"]) for name, data in ranked],
        })

    print(f"\n\n{'=' * 70}")
    print("  SUMMARY: MODEL RANKINGS ACROSS ALL TESTS")
    print(f"{'=' * 70}")

    model_wins = {}
    for result in all_results:
        if result["rankings"]:
            winner = result["rankings"][0][0]
            model_wins[winner] = model_wins.get(winner, 0) + 1

    for model, wins in sorted(model_wins.items(), key=lambda x: x[1], reverse=True):
        print(f"  {model}: {wins} wins out of {len(all_results)} tests")

    return all_results


def run_test_suite():                                      # 👈 único asyncio.run del programa
    return asyncio.run(run_test_suite_async())