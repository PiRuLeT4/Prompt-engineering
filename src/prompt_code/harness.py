import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

MODEL_CONFIGS = {
    "gpt-6-luna": {
        "provider": "openai",
        "model": "gpt-6-luna",
        "max_tokens": 2048,
        "context_window": 128_000,
    },
    "claude-haiku-5-5": {
        "provider": "anthropic",
        "model": "claude-haiku-5-5",
        "max_tokens": 2048,
        "context_window": 1_000_000,
    },
}

async def call_real_llm_async(model_name, prompt):
    """
    Makes a real call to any LLM provider using universal abstraction on LangChain
    """
    config = MODEL_CONFIGS[model_name]

    model_kwargs = {
        "model": config["model"],
        "model_provider": config["provider"],
        "max_tokens": config["max_tokens"],
    }

    # if config["provider"] != "anthropic" or config["provider"] != "openai":
    #     model_kwargs["temperature"] = float(prompt.get("temperature", 0))

    llm = init_chat_model(**model_kwargs)

    messages = [
        SystemMessage(content=prompt["system"]),
        HumanMessage(content=prompt["user"]),
    ]

    start_time = time.time()
    ai_message = await llm.ainvoke(messages)
    latency_ms = (time.time() - start_time) * 1000

    content = ai_message.content
    if isinstance(content, list):
        text_parts = [
            part["text"] for part in content if isinstance(part, dict) and "text" in part
        ]
        text_response = "\n".join(text_parts) if text_parts else str(content)
    else:
        text_response = str(content)

    #.. tokens used
    tokens_used = {}
    usage = getattr(ai_message, "usage_metadata", None)
    if usage:
        tokens_used = {
            "prompt": usage.get("input_tokens", 0),
            "completion": usage.get("output_tokens", 0),
            "total": usage.get("total_tokens", 0)
        }
    meta = getattr(ai_message, "response_metadata", {})

    finish_reason = meta.get("finish_reason") or meta.get("stop_reason") or "completed"

    return {
        "response": text_response,
        "tokens_used": tokens_used,
        "latency_ms": round(latency_ms, 2),
        "finish_reason": finish_reason
    }


async def run_prompt_test_async(prompt, models=None):
    if models is None:
        models = list(MODEL_CONFIGS.keys())

    tasks = [call_real_llm_async(model_name, prompt) for model_name in models]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = {}
    for model_name, response in zip(models, responses):
        if isinstance(response, Exception):
            results[model_name] = {
                "response": f"[ERROR] {type(response).__name__}: {response}",
                "tokens": {},
                "api_latency_ms": 0,
                "finish_reason": "error",
            }
        else:
            results[model_name] = {
                "response": response["response"],
                "tokens": response["tokens_used"],
                "api_latency_ms": response["latency_ms"],
                "finish_reason": response.get("finish_reason"),
            }
    return results


def run_prompt_test(prompt, models=None):
    return asyncio.run(run_prompt_test_async(prompt, models))