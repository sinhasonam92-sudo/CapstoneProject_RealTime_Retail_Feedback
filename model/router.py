from config import client, CHAT_MODEL


def generate_customer_response(sentiment, rating, analysis):

    if sentiment == "Positive":

        system_prompt = """
You are a retail customer support assistant.

Generate a warm thank-you message.

Mention the product.

Keep it under 70 words.

Encourage future purchases.
"""

    elif sentiment == "Neutral":

        system_prompt = """
You are a retail customer support assistant.

Generate a polite acknowledgement.

Mention the product.

Appreciate the feedback.

Keep under 70 words.
"""

    else:

        system_prompt = """
You are a retail customer support assistant.

Apologize sincerely.

Mention the product.

Inform the customer that a support team member will contact them soon.

Keep under 70 words.

Be empathetic.
"""

    user_prompt = f"""

Product:
{analysis['product']}

Category:
{analysis['category']}

Department:
{analysis['department']}

Urgency:
{analysis['urgency']}

Summary:
{analysis['summary']}

Estimated Rating:
{rating}
"""

    response = client.chat.completions.create(

        model=CHAT_MODEL,

        temperature=0.7,

        messages=[

            {
                "role":"system",
                "content":system_prompt
            },

            {
                "role":"user",
                "content":user_prompt
            }

        ]

    )

    return response.choices[0].message.content