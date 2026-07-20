"""
-------------------------------------------------------

File : report_generator.py

Purpose:
Generate structured retail reports.

Features
--------
✔ Customer metadata
✔ RoBERTa sentiment
✔ LLM Zero Shot analysis
✔ LLM Few Shot analysis
✔ LLM COT analysis
✔ Backend Category
✔ Business Insight
✔ Auto Save CSV

-------------------------------------------------------
"""

import os
import logging
from datetime import datetime

import pandas as pd


logger = logging.getLogger(__name__)


# -------------------------------------------------------
# Reports Folder
# -------------------------------------------------------

REPORT_FOLDER = "reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# -------------------------------------------------------
# Generate Report
# -------------------------------------------------------

def generate_report(
    age,
    recommended,
    division,
    department,
    product_class,
    review,
    bert_result,
    analysis,
):

    """
    Generate retail feedback report.

    Parameters
    ----------
    age : str
        Customer age

    recommended : str
        Recommend product or not

    division : str
        Product division

    department : str
        Product department

    product_class : str
        Product class

    review : str
        Customer review

    bert_result : dict
        RoBERTa sentiment output

    analysis : dict
        LLM analysis output

    Returns
    -------
    pandas.DataFrame
    """

    try:

        # -----------------------------------------------
        # Extract LLM outputs
        # -----------------------------------------------

        zero_shot = analysis.get(
            "zero_shot",
            {}
        )

        few_shot = analysis.get(
            "few_shot",
            {}
        )

        cot = analysis.get(
            "cot",
            {}
        )


        # -----------------------------------------------
        # Create Report
        # -----------------------------------------------

        report = {


            "Timestamp":

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),


            # Customer Information

            "Age":
                age,


            "Recommended":

                recommended,


            "Division":

                division,


            "Department":

                department,


            "Product Class":

                product_class,


            "Customer Review":

                review,



            # -------------------------------------------
            # RoBERTa Sentiment
            # -------------------------------------------

            "RoBERTa Sentiment":

                bert_result.get(
                    "sentiment",
                    ""
                ),


            "RoBERTa Confidence":

                bert_result.get(
                    "confidence",
                    0
                ),



            # -------------------------------------------
            # LLM Comparison
            # -------------------------------------------

            "LLM Zero Shot":

                str(zero_shot),


            "LLM Few Shot":

                str(few_shot),


            "LLM Chain of Thought":

                str(cot),



            # -------------------------------------------
            # Final Business Analysis
            # Using Zero Shot as primary output
            # -------------------------------------------


            "Predicted Rating":

                zero_shot.get(
                    "predicted_rating",
                    ""
                ),



            "Overall Sentiment":

                zero_shot.get(
                    "overall_sentiment",
                    ""
                ),



            "Aspect Sentiments":

                str(
                    zero_shot.get(
                        "aspect_sentiments",
                        []
                    )
                ),



            "Backend Priority":

                zero_shot.get(
                    "backend_priority",
                    ""
                ),



            "Backend Category":

                zero_shot.get(
                    "backend_category",
                    ""
                ),



            "Backend Action":

                zero_shot.get(
                    "backend_action",
                    ""
                ),



            "Customer Response":

                zero_shot.get(
                    "customer_response",
                    ""
                ),



            "Review Summary":

                zero_shot.get(
                    "review_summary",
                    ""
                ),



            "Business Insight":

                zero_shot.get(
                    "business_insight",
                    ""
                ),

        }



        # -----------------------------------------------
        # DataFrame
        # -----------------------------------------------

        df = pd.DataFrame(
            [report]
        )



        # -----------------------------------------------
        # Save CSV
        # -----------------------------------------------

        filename = os.path.join(

            REPORT_FOLDER,

            f"Retail_Report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        )


        df.to_csv(

            filename,

            index=False

        )


        logger.info(
            f"Report saved to {filename}"
        )


        return df



    except Exception as e:

        logger.exception(e)

        return pd.DataFrame()