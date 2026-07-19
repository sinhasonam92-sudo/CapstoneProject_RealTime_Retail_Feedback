"""
-------------------------------------------------------

File : app.py (Part 1)

Retail Feedback Analyzer

Part 1
------
✓ Imports
✓ Page Configuration
✓ Session State
✓ Sidebar
✓ File Upload
✓ Helper Functions

-------------------------------------------------------
"""

import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from model.llm_analysis import analyze_review


from utils.report_generator import generate_report

from model.llm_sentiment import (
    predict_zero_shot,
    predict_few_shot,
    predict_chain_of_thought,
)

if "batch_results" not in st.session_state:
    st.session_state.batch_results = pd.DataFrame()
# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Retail Feedback Analyzer",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------

st.markdown(
    """
<style>

.main-title{
    font-size:38px;
    font-weight:700;
    color:#1F618D;
}

.subtitle{
    font-size:18px;
    color:gray;
}

.metric-card{
    background:#F4F6F7;
    padding:18px;
    border-radius:10px;
    border:1px solid #D6DBDF;
}

div.stButton > button{
    width:100%;
}

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown(
    "<p class='main-title'>🛍️ Retail Feedback Analyzer</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p class='subtitle'>"
    "Analyze customer reviews using Azure OpenAI"
    "</p>",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    uploaded_file = st.file_uploader(
        "Upload CSV / Excel",
        type=["csv", "xlsx"],
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Choose Mode",
        [
            "Single Review",
            "Batch Analysis",
            "Analytics Dashboard",
        ],
    )

    st.divider()


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def load_dataset(file):
    """
    Load CSV or Excel dataset.
    """

    if file is None:
        return None

    suffix = Path(file.name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file)

    if suffix == ".xlsx":
        return pd.read_excel(file)

    return None


def detect_review_column(df):
    """
    Return all available review columns (case-insensitive).
    """

    # Allowed review columns
    candidates = [
        "title",
        "review_text",
        "full_review"
    ]

    # Create mapping: lowercase -> original column name
    df_columns_lower = {
        col.lower(): col
        for col in df.columns
    }

    available = []

    for col in candidates:

        if col in df_columns_lower:

            # Append original column name from dataframe
            available.append(df_columns_lower[col])

    return available

def safe_value(row, column, default=None):
    """
    Safely fetch dataframe value.
    """

    if column in row.index:
        return row[column]

    return default



def show_metric(label, value):

    st.metric(label, value)


# -------------------------------------------------------
# Load Uploaded Dataset
# -------------------------------------------------------

dataset = None

if uploaded_file is not None:

    dataset = load_dataset(uploaded_file)

    if dataset is not None:

        st.sidebar.success(
            f"Loaded {len(dataset)} records."
        )

    else:

        st.sidebar.error(
            "Unsupported file format."
        )
# -------------------------------------------------------
# Single Review Analysis
# -------------------------------------------------------

if page == "Single Review":

    st.header("📝 Single Review Analysis")

    with st.form("single_review_form"):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Customer Age",
                min_value=18,
                max_value=100,
                value=35,
            )

            recommended = st.selectbox(
                "Recommended Product?",
                ["Yes", "No"],
            )

        with col2:

            division = st.selectbox(
                "Division",
                options=[
                    "Select Any",
                    "Initmates",
                    "General",
                    "General Petite",   
                    "Others"
                    
                ],
            )

            department = st.selectbox(
                "Department",
                options=[
                    "Select Any",
                    "Intimate",
                    "Dresses",
                    "Bottoms"
                    "Tops",
                    "Jackets",
                    "Others"
                ]
            )

            product_class = st.selectbox(
                "product_class",
                options=[
                    "Select Any","Intimates" ,"Dresses",
                    "Pants", "Blouses", "Knits", "Outerwear", "Lounge",
                    "Sweaters" ,"Skirts" ,"Fine gauge" ,"Sleep","Other"
                ]
            )

        review = st.text_area(
            "Customer Review",
            height=180,
            placeholder="Enter customer review here...",
        )

        analyze_btn = st.form_submit_button(
            "🔍 Analyze Review"
        )

    # -------------------------------------------------------
    # Analyze Button
    # -------------------------------------------------------

    if analyze_btn:

        if review.strip() == "":

            st.warning("Please enter a customer review.")

        else:

            with st.spinner("Analyzing review..."):

                try:

                    # ------------------------------------
                    # Sentiment Analysis
                    # ------------------------------------

                    # Zero-Shot
                    zero_result = predict_zero_shot(review)
                    
                    # Few-Shot
                    few_result = predict_few_shot(review)
                    
                    # Chain-of-Thought
                    cot_result = predict_chain_of_thought(review)
                    
                    # -------------------------------------------------------
                    # Store all predictions
                    # -------------------------------------------------------
                    
                    all_predictions = {
                        "Zero-Shot": zero_result["sentiment"],
                        "Few-Shot": few_result["sentiment"],
                        "Chain-of-Thought": cot_result["sentiment"],
                    }
                    
                    # Use Chain-of-Thought as the final sentiment
                    final_sentiment = all_predictions["Chain-of-Thought"]
                    st.success("Analysis Completed Successfully!")
                    # ------------------------------------
                    # Azure OpenAI Analysis
                    # ------------------------------------

                    analysis = analyze_review(
                        age=age,
                        recommended=recommended,
                        division=division,
                        department=department,
                        product_class=product_class,
                        review=review,
                    )

                    # ------------------------------------
                    # Display Metrics
                    # ------------------------------------

                    st.success("Analysis Completed Successfully!")
                    # -------------------------------------------------------
                    # LLM Sentiment Predictions
                    # -------------------------------------------------------
                    
                    st.subheader("📊 LLM Sentiment Predictions")
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                    
                        st.markdown("### Zero-Shot")
                    
                        st.metric(
                            "Prediction",
                            zero_result["sentiment"]
                        )
                    
                    with c2:
                    
                        st.markdown("### Few-Shot")
                    
                        st.metric(
                            "Prediction",
                            few_result["sentiment"]
                        )
                    
                    with c3:
                    
                        st.markdown("### Chain-of-Thought")
                    
                        st.metric(
                            "Prediction",
                            cot_result["sentiment"]
                        )
                    
                    st.divider()
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(
                            "Estimated Rating",
                            f"{analysis['estimated_rating']}/5"
                        )
                
                    with m2:
                        st.metric(
                            "Final Sentiment",
                            final_sentiment
                        )
                
                    with  m3:
                        st.metric(
                            "Urgency",
                            analysis["urgency"]
                        )
                    st.divider()

                    left, right = st.columns(2)

                    with left:

                        st.subheader("📦 Product Details")

                        st.write(
                            "**Product:**",
                            analysis["product"],
                        )

                        st.write(
                            "**Category:**",
                            analysis["category"],
                        )

                        st.write(
                            "**Department:**",
                            analysis["department"],
                        )

                    with right:

                        st.subheader("📋 AI Summary")

                        st.info(
                            analysis["summary"]
                        )

                        st.subheader(
                            "✅ Recommended Action"
                        )

                        st.success(
                            analysis["recommended_action"]
                        )

                    # ------------------------------------
                    # Generate Report
                    # ------------------------------------

                    report_df = generate_report(
                        age=age,
                        recommended=recommended,
                        division=division,
                        department=department,
                        product_class=product_class,
                        review=review,
                        bert_result={
                            "sentiment": cot_result["sentiment"],
                        },
                        analysis=analysis,
                    )


                    st.download_button(
                        label="⬇ Download Current Report (CSV)",
                        data=report_df.to_csv(index=False),
                        file_name="Retail_Report.csv",
                        mime="text/csv",
                    )

                except Exception as e:

                    st.exception(e)

# -------------------------------------------------------
# Batch Review Analysis
# -------------------------------------------------------

elif page == "Batch Analysis":

    st.header("📊 Batch Review Analysis")

    if dataset is None:

        st.info("Please upload a CSV or Excel file from the sidebar.")

    else:

        st.success(f"Dataset Loaded Successfully ({len(dataset)} records)")

        st.dataframe(dataset.head())

        available_review_columns = detect_review_column(dataset)
        
        if not available_review_columns:
        
            st.error(
                "No valid review column found. Please include one of: "
                "Title, Review_Text, Full_Review"
            )
        
            st.stop()
        
        review_column = st.selectbox(
            "Select Review Column",
            options=available_review_columns,
            index=0
        )
        
        st.write(f"**Review Column:** {review_column}")

        if st.button("🚀 Analyze Dataset"):

            results = []

            progress_bar = st.progress(0)

            status = st.empty()

            total_rows = len(dataset)

            for index, row in dataset.iterrows():

                status.text(
                    f"Processing Review {index + 1} of {total_rows}"
                )

                review = str(
                    safe_value(
                        row,
                        review_column,
                        ""
                    )
                )

                zero_result = predict_zero_shot(review)
                few_result = predict_few_shot(review)
                cot_result = predict_chain_of_thought(review)

                try:

                    analysis = analyze_review(

                        age=safe_value(
                            row,
                            "Age",
                            0
                        ),

                        recommended=safe_value(
                            row,
                            "Recommended IND",
                            "Unknown"
                        ),

                        division=safe_value(
                            row,
                            "Division Name",
                            "Unknown"
                        ),

                        department=safe_value(
                            row,
                            "Department Name",
                            "Unknown"
                        ),

                        product_class=safe_value(
                            row,
                            "Class Name",
                            "Unknown"
                        ),

                        review=review,

                    )

                except Exception as e:

                    st.error(e)

                    analysis = {

                        "estimated_rating": 3,
                        "product": "Unknown",
                        "category": "Unknown",
                        "department": "Unknown",
                        "urgency": "Low",
                        "summary": "Analysis failed.",
                        "recommended_action": "Manual Review"

                    }

                report = {

                    "Age":
                        safe_value(row, "Age", ""),

                    "Recommended":
                        safe_value(
                            row,
                            "Recommended IND",
                            ""
                        ),


                    "Division":
                        safe_value(
                            row,
                            "Division Name",
                            ""
                        ),

                    "Department":
                        safe_value(
                            row,
                            "Department Name",
                            ""
                        ),

                    "Product Class":
                        safe_value(
                            row,
                            "Class Name",
                            ""
                        ),

                    "Customer Review":
                        review,

                    "Zero-Shot": zero_result["sentiment"],
                    "Few-Shot": few_result["sentiment"],
                    "Chain-of-Thought": cot_result["sentiment"],
                    
                    # Final sentiment (use CoT)
                    "Sentiment": cot_result["sentiment"],

                    "Estimated Rating":
                        analysis["estimated_rating"],

                    "Product":
                        analysis["product"],

                    "Category":
                        analysis["category"],

                    "Detected Department":
                        analysis["department"],

                    "Urgency":
                        analysis["urgency"],

                    "Summary":
                        analysis["summary"],

                    "Recommended Action":
                        analysis["recommended_action"],

                }

                results.append(report)

                progress_bar.progress(
                    (index + 1) / total_rows
                )

            status.success("✅ Batch Analysis Completed")

            results_df = pd.DataFrame(results)

            st.session_state.batch_results = results_df

            st.subheader("📄 Analysis Results")

            st.dataframe(
                results_df,
                use_container_width=True
            )

            # ---------------------------------------
            # Summary Metrics
            # ---------------------------------------

            st.subheader("📈 Summary")

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "Total Reviews",
                    len(results_df)
                )

            with c2:

                positive = len(

                    results_df[
                        results_df["Sentiment"] == "Positive"
                    ]

                )

                st.metric(
                    "Positive",
                    positive
                )

            with c3:

                negative = len(

                    results_df[
                        results_df["Sentiment"] == "Negative"
                    ]

                )

                st.metric(
                    "Negative",
                    negative
                )

            with c4:

                urgent = len(

                    results_df[
                        results_df["Urgency"] == "High"
                    ]

                )

                st.metric(
                    "High Urgency",
                    urgent
                )

            # ---------------------------------------
            # Download Results
            # ---------------------------------------

            csv = results_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(

                label="⬇ Download Analysis Report",

                data=csv,

                file_name="Retail_Feedback_Analysis.csv",

                mime="text/csv",

            )

            # ---------------------------------------
            # Auto Save Individual Reports
            # ---------------------------------------

            with st.spinner(
                "Saving reports..."
            ):

                for _, row in results_df.iterrows():

                    generate_report(

                        age=row["Age"],

                        recommended=row["Recommended"],

                        division=row["Division"],

                        department=row["Department"],

                        product_class=row["Product Class"],

                        review=row["Customer Review"],

                        bert_result={

                            "sentiment":
                                row["Sentiment"],


                        },

                        analysis={

                            "estimated_rating":
                                row["Estimated Rating"],

                            "product":
                                row["Product"],

                            "category":
                                row["Category"],

                            "department":
                                row["Detected Department"],

                            "urgency":
                                row["Urgency"],

                            "summary":
                                row["Summary"],

                            "recommended_action":
                                row["Recommended Action"]

                        }

                    )

            st.success(
                "Reports saved successfully in the reports folder."
            )

# -------------------------------------------------------
# Analytics Dashboard
# -------------------------------------------------------

elif page == "Analytics Dashboard":

    st.header("📊 Retail Analytics Dashboard")

    if st.session_state.batch_results.empty:

        st.info(
            "No batch analysis available.\n\n"
            "Please analyze a dataset first."
        )

    else:

        df = st.session_state.batch_results.copy()

        # ---------------------------------------------------
        # Filters
        # ---------------------------------------------------

        st.sidebar.subheader("Dashboard Filters")

        sentiment_filter = st.sidebar.multiselect(
            "Sentiment",
            options=sorted(df["Sentiment"].dropna().unique()),
            default=sorted(df["Sentiment"].dropna().unique()),
        )

        urgency_filter = st.sidebar.multiselect(
            "Urgency",
            options=sorted(df["Urgency"].dropna().unique()),
            default=sorted(df["Urgency"].dropna().unique()),
        )

        department_filter = st.sidebar.multiselect(
            "Department",
            options=sorted(df["Detected Department"].dropna().unique()),
            default=sorted(df["Detected Department"].dropna().unique()),
        )

        filtered_df = df[
            (df["Sentiment"].isin(sentiment_filter))
            &
            (df["Urgency"].isin(urgency_filter))
            &
            (df["Detected Department"].isin(department_filter))
        ]

        st.success(
            f"Showing {len(filtered_df)} of {len(df)} reviews"
        )

        # ---------------------------------------------------
        # KPI Metrics
        # ---------------------------------------------------

        st.subheader("📈 Key Performance Indicators")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Total Reviews",
                len(filtered_df)
            )

        with c2:

            avg_rating = round(
                filtered_df["Estimated Rating"].mean(),
                2
            )

            st.metric(
                "Average Rating",
                avg_rating
            )

        with c3:

            high = len(
                filtered_df[
                    filtered_df["Urgency"] == "High"
                ]
            )

            st.metric(
                "High Urgency",
                high
            )

        st.divider()

        # ---------------------------------------------------
        # Charts
        # ---------------------------------------------------

        chart1, chart2 = st.columns(2)

        with chart1:

            st.subheader("Sentiment Distribution")

            sentiment_chart = (
                filtered_df["Sentiment"]
                .value_counts()
            )

            st.bar_chart(sentiment_chart)

        with chart2:

            st.subheader("Urgency Distribution")

            urgency_chart = (
                filtered_df["Urgency"]
                .value_counts()
            )

            st.bar_chart(urgency_chart)

        chart3, chart4 = st.columns(2)

        with chart3:

            st.subheader("Department Distribution")

            dept_chart = (
                filtered_df["Detected Department"]
                .value_counts()
            )

            st.bar_chart(dept_chart)

        with chart4:

            st.subheader("Category Distribution")

            category_chart = (
                filtered_df["Category"]
                .value_counts()
            )

            st.bar_chart(category_chart)

        # ---------------------------------------------------
        # Rating Analysis
        # ---------------------------------------------------

        st.subheader("⭐ Rating Distribution")

        rating_chart = (
            filtered_df["Estimated Rating"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(rating_chart)

        # ---------------------------------------------------
        # Product Analysis
        # ---------------------------------------------------

        st.subheader("🛍️ Top Products")

        top_products = (
            filtered_df["Product"]
            .value_counts()
            .head(10)
        )

        st.bar_chart(top_products)

        # ---------------------------------------------------
        # Search Reviews
        # ---------------------------------------------------

        st.subheader("🔍 Search Reviews")

        keyword = st.text_input(
            "Search keyword"
        )

        if keyword:

            search_df = filtered_df[
                filtered_df["Customer Review"]
                .str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ]

            st.write(
                f"{len(search_df)} matching reviews found."
            )

            st.dataframe(
                search_df,
                use_container_width=True
            )

        # ---------------------------------------------------
        # High Priority Cases
        # ---------------------------------------------------

        st.subheader("🚨 High Priority Reviews")

        urgent_df = filtered_df[
            filtered_df["Urgency"] == "High"
        ]

        if len(urgent_df):

            st.dataframe(
                urgent_df,
                use_container_width=True
            )

        else:

            st.success(
                "No high-priority reviews found."
            )

        # ---------------------------------------------------
        # Detailed Results
        # ---------------------------------------------------

        st.subheader("📄 Complete Analysis")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500
        )

        # ---------------------------------------------------
        # Download Filtered Dataset
        # ---------------------------------------------------

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            "⬇ Download Filtered Results",

            data=csv,

            file_name="Filtered_Retail_Report.csv",

            mime="text/csv"

        )


# -------------------------------------------------------
# Recent Batch Results
# -------------------------------------------------------

if not st.session_state.batch_results.empty:

    st.divider()

    st.header("📊 Recent Batch Analysis")

    st.dataframe(

        st.session_state.batch_results,

        use_container_width=True,

        height=400,

    )

# -------------------------------------------------------
# Business Insights
# -------------------------------------------------------

if not st.session_state.batch_results.empty:

    df = st.session_state.batch_results

    st.divider()

    st.header("💡 AI Business Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Categories")

        st.table(

            df["Category"]

            .value_counts()

            .head(10)

            .rename("Reviews")

        )

    with col2:

        st.subheader("Top Departments")

        st.table(

            df["Detected Department"]

            .value_counts()

            .head(10)

            .rename("Reviews")

        )

    st.subheader("Recommended Actions")

    actions = (

        df["Recommended Action"]

        .value_counts()

        .reset_index()

    )

    actions.columns = [

        "Action",

        "Frequency"

    ]

    st.dataframe(

        actions,

        use_container_width=True

    )


# -------------------------------------------------------
# End of Application
# -------------------------------------------------------