"""
-------------------------------------------------------

GPT Review Analyzer

Uses

Azure OpenAI
+
Pydantic Validation

-------------------------------------------------------
"""

import json
import logging

from config import client, CHAT_MODEL

from prompts.prompts import (
    SYSTEM_PROMPT,
    ANALYSIS_PROMPT
)

from model.schema import ReviewAnalysis


logger = logging.getLogger(__name__)


# -------------------------------------------------------
# Default Response
# -------------------------------------------------------

DEFAULT_ANALYSIS = ReviewAnalysis(

    estimated_rating=3,

    product="Unknown",

    category="Unknown",

    department="Unknown",

    urgency="Low",

    summary="Unable to analyze review.",

    recommended_action="Manual Review"

)


# -------------------------------------------------------
# Review Analysis
# -------------------------------------------------------

def analyze_review(

    age,

    recommended,

    division,

    department,

    product_class,

    review

):

    try:

        customer_context = f"""

        Customer Details
        
        Age : {age}
        
        Recommended : {recommended}
        
        Division : {division}
        
        Department : {department}
        
        Product Class : {product_class}
        
        Customer Review
        
        {review}
        
        """

        response = client.chat.completions.create(

            model=CHAT_MODEL,

            temperature=0,

            response_format={

                "type":"json_object"

            },

            messages=[

                {

                    "role":"system",

                    "content":SYSTEM_PROMPT

                },

                {

                    "role":"system",

                    "content":ANALYSIS_PROMPT

                },

                {

                    "role":"user",

                    "content":customer_context

                }

            ]

        )

        result = response.choices[0].message.content

        data = json.loads(result)

        analysis = ReviewAnalysis.model_validate(data)

        return analysis.model_dump()

    except Exception as e:

        logger.exception(e)

        return DEFAULT_ANALYSIS.model_dump()