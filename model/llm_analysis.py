import json
import time

from config import client, CHAT_MODEL
from prompts.prompts import (
    SYSTEM_PROMPT,
    ZERO_SHOT_PROMPT,
    FEW_SHOT_PROMPT,
    COT_PROMPT,
)


def run_llm_evaluation(prompt, technique_name, max_retries=3):
    start_time = time.time()

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )

            result = response.choices[0].message.content.strip()
            parsed = json.loads(result)
            default_fields = {

                "predicted_rating": "",
                "overall_sentiment": "",
                "aspect_sentiments": [],
            
                "backend_priority": "",
                "backend_category": "",
            
                "backend_action": "",
            
                "customer_response": "",
            
                "review_summary": "",
            
                "business_insight": ""
        
            }   
        
        
            for key, value in default_fields.items():
        
                parsed.setdefault(
                    key,
                    value
                )

            parsed["technique"] = technique_name
            parsed["model"] = CHAT_MODEL
            parsed["processing_time"] = round(time.time() - start_time, 2)

            return parsed

        except Exception as e:
            if attempt == max_retries - 1:
                return {
                    "technique": technique_name,
                    "error": str(e),
                    "processing_time": round(time.time() - start_time, 2),
                }

            time.sleep(2)


def analyze_feedback(review_text, department, product_class):

    zero_prompt = ZERO_SHOT_PROMPT.format(
        department=department,
        product_class=product_class,
        review=review_text,
    )

    few_prompt = FEW_SHOT_PROMPT.format(
        department=department,
        product_class=product_class,
        review=review_text,
    )

    cot_prompt = COT_PROMPT.format(
        department=department,
        product_class=product_class,
        review=review_text,
    )

    zero_result = run_llm_evaluation(zero_prompt, "Zero-Shot")
    few_result = run_llm_evaluation(few_prompt, "Few-Shot")
    cot_result = run_llm_evaluation(cot_prompt, "Chain-of-Thought")

    return {
        "zero_shot": zero_result,
        "few_shot": few_result,
        "cot": cot_result,
    }