"""
LLM Sentiment Analysis using Azure OpenAI

Methods:
- Zero-Shot
- Few-Shot
- Chain-of-Thought
"""

import logging

from config import client, CHAT_MODEL

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Prompts
# -------------------------------------------------------

ZERO_SHOT_PROMPT = """
Classify the sentiment of the customer review.

Return ONLY one label:

Positive
Negative
Neutral
"""

FEW_SHOT_PROMPT = """
You are an expert retail sentiment classifier.

Example 1
Review: This dress fits perfectly and the quality is excellent.
Sentiment: Positive

Example 2
Review: The stitching came apart after one wash and I want a refund.
Sentiment: Negative

Example 3
Review: The product is okay and delivery was average.
Sentiment: Neutral

Now classify the following review.

Return ONLY one label:

Positive
Negative
Neutral
"""

CHAIN_OF_THOUGHT_PROMPT = """
You are an expert retail sentiment analyst.

Think step by step:
1. Identify positive phrases.
2. Identify negative phrases.
3. Determine overall customer satisfaction.
4. Choose the final sentiment.

Return ONLY one label:

Positive
Negative
Neutral
"""

# -------------------------------------------------------
# Internal helper
# -------------------------------------------------------

def _call_llm(prompt: str, review: str) -> str:

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": review},
        ],
    )

    return response.choices[0].message.content.strip()

# -------------------------------------------------------
# Zero-Shot
# -------------------------------------------------------

def predict_zero_shot(review: str) -> dict:

    try:

        sentiment = _call_llm(
            ZERO_SHOT_PROMPT,
            review
        )

        return {
            "sentiment": sentiment
        }

    except Exception as e:

        logger.exception(e)

        return {
            "sentiment": "Unknown",
            "error": str(e)
        }

# -------------------------------------------------------
# Few-Shot
# -------------------------------------------------------

def predict_few_shot(review: str) -> dict:

    try:

        sentiment = _call_llm(
            FEW_SHOT_PROMPT,
            review
        )

        return {
            "sentiment": sentiment
        }

    except Exception as e:

        logger.exception(e)

        return {
            "sentiment": "Unknown",
            "error": str(e)
        }

# -------------------------------------------------------
# Chain-of-Thought
# -------------------------------------------------------

def predict_chain_of_thought(review: str) -> dict:

    try:

        sentiment = _call_llm(
            CHAIN_OF_THOUGHT_PROMPT,
            review
        )

        return {
            "sentiment": sentiment
        }

    except Exception as e:

        logger.exception(e)

        return {
            "sentiment": "Unknown",
            "error": str(e)
        }