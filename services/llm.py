import json
import logging
import re

from openai import AsyncOpenAI

import config
import prompts

logger = logging.getLogger(__name__)

_client = AsyncOpenAI(
    api_key=config.OPENROUTER_KEY,
    base_url=config.OPENROUTER_BASE_URL,
)


async def _chat(messages: list[dict]) -> str:
    """Send messages to the LLM and return the raw response text."""
    response = await _client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def _parse_json(text: str) -> dict:
    """Extract a JSON object from LLM response, with fallback regex parsing."""
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try extracting JSON block from markdown fences or surrounding text
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    logger.warning("Failed to parse JSON from LLM response: %s", text[:200])
    return {"satisfactory": False, "status": "unsatisfactory", "feedback": text, "reformatted_cv": "", "description": ""}


async def evaluate_cv(raw_text: str) -> dict:
    """Evaluate a CV. Returns {satisfactory, reformatted_cv, feedback}."""
    messages = prompts.evaluate_cv_messages(raw_text)
    raw = await _chat(messages)
    result = _parse_json(raw)
    return {
        "satisfactory": bool(result.get("satisfactory", False)),
        "reformatted_cv": result.get("reformatted_cv", ""),
        "feedback": result.get("feedback", ""),
    }


async def evaluate_company(raw_text: str) -> dict:
    """Evaluate a company description. Returns {satisfactory, description, feedback}."""
    messages = prompts.evaluate_company_messages(raw_text)
    raw = await _chat(messages)
    result = _parse_json(raw)
    return {
        "satisfactory": bool(result.get("satisfactory", False)),
        "description": result.get("description", ""),
        "feedback": result.get("feedback", ""),
    }


async def generate_question(
    cv: str, company: str, previous_qa: list[tuple[str, str]]
) -> str:
    """Generate the next interview question."""
    messages = prompts.generate_question_messages(cv, company, previous_qa)
    return await _chat(messages)


async def evaluate_answer(
    question: str, answer: str, cv: str, company: str
) -> dict:
    """Evaluate a candidate answer. Returns {status, feedback}.

    status is one of: 'satisfactory', 'unsatisfactory', 'offensive'.
    """
    messages = prompts.evaluate_answer_messages(question, answer, cv, company)
    raw = await _chat(messages)
    result = _parse_json(raw)
    status = result.get("status", "")
    # Fallback: support legacy satisfactory bool field
    if status not in ("satisfactory", "unsatisfactory", "offensive"):
        status = "satisfactory" if result.get("satisfactory", True) else "unsatisfactory"
    return {
        "status": status,
        "feedback": result.get("feedback", ""),
    }


async def check_offensive(text: str) -> bool:
    """Quick check if a message is offensive/impertinent."""
    messages = prompts.check_offensive_messages(text)
    raw = await _chat(messages)
    result = _parse_json(raw)
    return bool(result.get("offensive", False))


async def generate_beast_response(
    user_message: str,
    cv: str,
    company: str,
    beast_history: list[tuple[str, str]],
) -> str:
    """Generate a beast-mode roast response."""
    messages = prompts.generate_beast_response_messages(
        user_message, cv, company, beast_history
    )
    return await _chat(messages)


async def generate_report(
    cv: str, company: str, qa_pairs: list[tuple[str, str]]
) -> str:
    """Generate the final interview report."""
    messages = prompts.generate_report_messages(cv, company, qa_pairs)
    return await _chat(messages)
