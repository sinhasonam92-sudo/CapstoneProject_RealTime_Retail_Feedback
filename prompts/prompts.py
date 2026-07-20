SYSTEM_PROMPT = """
You are an AI-powered Retail Feedback Intelligence System for ChicStyle, an online women's fashion retailer.

Your responsibilities are to:

1. Estimate the customer's rating on a scale of 1–5.
2. Determine the customer's overall sentiment.
3. Identify every important product aspect discussed.
4. Assign a sentiment to each identified aspect.
5. Determine whether the issue requires backend action.
6. Categorize the backend task.
7. Recommend an appropriate backend action.
8. Generate a professional and empathetic response to the customer.
9. Summarize the review.
10. Derive one concise business insight.

Retailer characteristics:

- Customers generally provide positive ratings.
- Minor sizing issues often still receive good ratings.
- Reviews usually discuss fabric, comfort, fit, color, appearance and quality.
- Ratings below 3 generally indicate multiple significant product issues.

Rating guidelines:

5:
Strong positive feedback, no issues.

4:
Positive feedback with minor issues.

3:
Mixed experience, noticeable issues but acceptable.

2:
Multiple problems affecting satisfaction.

1:
Severe dissatisfaction, product failure, or major quality issue.

Always return ONLY valid JSON.

Do not include Markdown.

Do not include explanations outside JSON.
"""

TASK_INSTRUCTION = """
Analyze the following customer review.

Customer Information

Department:
{department}

Product Class:
{product_class}

Customer Review:
{review}

Return ONLY a valid JSON object containing the following fields.

1. predicted_rating
   - Integer between 1 and 5

2. overall_sentiment
   - One of:
     Positive
     Mixed
     Negative

3. aspect_sentiments
   - List all important aspects mentioned in the review.
   - Use ONLY the following aspect names whenever applicable:
     • Sizing
     • Fabric
     • Comfort
     • Quality
     • Color
     • Appearance
     • Design
     • Durability
     • Other
   - Each aspect should have one sentiment:
     Positive
     Mixed
     Negative

4. backend_priority
   - One of:
     Low
     Medium
     High

5. backend_category
   - Use ONLY one of:
     Sizing
     Fabric
     Quality
     Comfort
     Color
     Appearance
     Design
     Durability
     Other

6. backend_action
   - Recommend one practical action for the retailer.

7. customer_response
   - Write a professional response consisting of:
     - Appreciation
     - Empathy (if applicable)
     - Action being taken
     - Closing statement

8. review_summary
   - Summarize the review in one concise sentence.

9. business_insight
   - Derive one concise business insight that could help improve products or customer experience.

Return ONLY valid JSON.

Do not include explanations.

Do not include Markdown.
"""

# ============================================================
# Common Task Instruction (Alternative/Template)
# ============================================================

COMMON_TASK = """
Analyze the following customer review and return ONLY valid JSON.

Customer Information

Department:
{department}

Product Class:
{product_class}

Customer Review:
{review}

Return the following JSON fields.

{
    "predicted_rating": Integer between 1 and 5,

    "overall_sentiment":
        "Positive"
        or
        "Mixed"
        or
        "Negative",

    "aspect_sentiments":[
        {
            "aspect":"...",
            "sentiment":"Positive | Mixed | Negative"
        }
    ],

    "backend_priority":
        "Low"
        or
        "Medium"
        or
        "High",

    "backend_category":
        "Sizing"
        or
        "Fabric"
        or
        "Quality"
        or
        "Comfort"
        or
        "Color"
        or
        "Appearance"
        or
        "Design"
        or
        "Other",

    "backend_action":"...",

    "customer_response":"...",

    "review_summary":"...",

    "business_insight":"..."
}

Return ONLY valid JSON.

Do not include explanations.

Do not include markdown.
"""

# ============================================================
# Zero-Shot Prompt
# ============================================================

ZERO_SHOT_PROMPT = TASK_INSTRUCTION

# ============================================================
# Few-Shot Context (as generated in notebook)
# ============================================================

FEW_SHOT_CONTEXT = """
Example

Department: Bottoms
Product Class: Jeans

Customer Review:
Cute jeans, terrible quality! I've purchased pilcro jeans in the past and they've held up great. unfortunately, the material used for this particular jean is a far, far cry from what it used to be. the thighs of these jeans start pilling (yes pilling!) after just a few wears. i've never had jeans do this -- whatever denim blend they are using is a complete disaster.

don't buy these -- you will be very disappointed.

Actual Rating:
1

----------------------------------------

Example

Department: Dresses
Product Class: Dresses

Customer Review:
Poor quality This is another item i've been stalking that i thought miraculously made it to sale with my size still available. i ordered online but when it arrived i have to be honest i didn't even try it on because i knew it would be going back. the beautiful print online looks really cheap irl on the flimsy fabric. the beaded detail on neck is basically a low grade sequin trim. so much potential just executed poorly.

Actual Rating:
2

----------------------------------------

Example

Department: Tops
Product Class: Sweaters

Customer Review:
Lovely colors and concept but fit is off I thought this was such a beautiful cardigan from the online photos. i ordered it in the small size but the fit is strange. the arms and wrist cuffs are so large it cannot be pushed up to stay out of the way for things i would like to do when wearing it (i'm a teacher and my classroom is that kind of environment). i was also confused by the front "collar" ribbing and how it was supposed to lay - open, folded over, partly folded over - it just didn't seem to have a particular style to this area.

Actual Rating:
3

----------------------------------------

Example

Department: Intimate
Product Class: Lounge

Customer Review:
Cute and so soft Great for lounging or running errands. can be dressed up or down. i found them to run at least a size large though.

Actual Rating:
4

----------------------------------------

Example

Department: Tops
Product Class: Blouses

Customer Review:
Comfy and classy This shirt is so soft and luxuriously feeling. the material looks very nice and seems well made. it has a nice length to it, so it can be worn properly with leggings without any worry. i'm a 36d and can't get the button to close properly, so i'd recommend sizing up if this could be an issue for you. overall it will be a very versitile piece i'm excited to add to my wardrobe.

Actual Rating:
5

----------------------------------------
"""

# ============================================================
# Few-Shot Prompt
# ============================================================

FEW_SHOT_PROMPT = f"""
Below are representative examples from ChicStyle customer reviews.

Use these examples to understand how customers of this retailer typically rate products.

{FEW_SHOT_CONTEXT}

Now analyze the following customer review.

{TASK_INSTRUCTION}
"""

# ============================================================
# Chain-of-Thought Prompt
# ============================================================

COT_PROMPT = """
Before generating the final JSON, internally reason through the following steps.

Step 1
Identify every important product aspect mentioned.

Step 2
Assign sentiment to every aspect.

Step 3
Determine the customer's overall satisfaction.

Step 4
Estimate the most appropriate rating.

Step 5
Determine backend priority.

Step 6
Recommend backend action.

Step 7
Generate customer response.

After completing the reasoning internally, return ONLY the required JSON.

""" + TASK_INSTRUCTION