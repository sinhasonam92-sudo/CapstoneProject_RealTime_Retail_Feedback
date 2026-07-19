"""
-------------------------------------------------------

File : config.py

Purpose:
Central configuration for the Retail Feedback Analyzer.

Loads environment variables and initializes the
Azure OpenAI client.

-------------------------------------------------------
"""

import os
import logging

from dotenv import load_dotenv
from openai import AzureOpenAI

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

# ----------------------------------------------------
# Logging Configuration
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# Environment Variables
# ----------------------------------------------------

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

# ----------------------------------------------------
# Validate Environment Variables
# ----------------------------------------------------

required_variables = {
    "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
    "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
    "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION,
}

missing = [
    key
    for key, value in required_variables.items()
    if not value
]

if missing:
    raise EnvironmentError(
        f"Missing environment variables: {', '.join(missing)}"
    )

# ----------------------------------------------------
# Azure OpenAI Client
# ----------------------------------------------------

try:

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    logger.info("Azure OpenAI client initialized successfully.")

except Exception as e:

    logger.exception("Failed to initialize Azure OpenAI client.")

    raise e