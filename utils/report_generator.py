"""
-------------------------------------------------------

File : report_generator.py

Purpose:
Generate structured retail reports.

Features
--------
✔ Customer metadata
✔ Sentiment
✔ Confidence
✔ Estimated Rating
✔ Product
✔ Category
✔ Department
✔ Urgency
✔ Summary
✔ Recommended Action
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
    Generate retail report.

    Parameters
    ----------

    age

    recommended

    helpful_votes

    division

    department

    product_class

    review

    bert_result

    analysis

    Returns
    -------

    pandas.DataFrame
    """

    try:

        report = {

            "Timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "Age":
                age,

            "Recommended":
                recommended,

            "Helpful Votes":
                helpful_votes,

            "Division":
                division,

            "Department":
                department,

            "Product Class":
                product_class,

            "Customer Review":
                review,

            "LLM Zero Shot":
                zero_shot,

"LLM Few Shot":
few_shot,

            "Confidence":
                bert_result.get(
                    "confidence",
                    0
                ),

            "Estimated Rating":
                analysis.get(
                    "estimated_rating",
                    3
                ),

            "Product":
                analysis.get(
                    "product",
                    "Unknown"
                ),

            "Category":
                analysis.get(
                    "category",
                    "Unknown"
                ),

            "Detected Department":
                analysis.get(
                    "department",
                    department
                ),

            "Urgency":
                analysis.get(
                    "urgency",
                    "Low"
                ),

            "Summary":
                analysis.get(
                    "summary",
                    ""
                ),

            "Recommended Action":
                analysis.get(
                    "recommended_action",
                    ""
                )

        }

        df = pd.DataFrame([report])

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