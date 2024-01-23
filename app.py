# Importing necessary libraries
import streamlit as st
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, iscr, borrowing_to_revenue_flag
import json

def initialize_session_state():
    
    if "results" not in st.session_state:
        st.session_state.results = None

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

def main():
    st.title("Financial Analysis Web App")

    # Initialize st.session_state
    initialize_session_state()

    # Page 1: Upload data.json and get results
    uploaded_file = st.file_uploader("Upload data.json", type=["json"])

    if uploaded_file is not None:
        st.write("Calculating results...")

       # Use probe_model_5l_profit to get results
        data = json.loads(uploaded_file.read().decode("utf-8"))
        results = probe_model_5l_profit(data["data"])

        st.success("Calculation completed!")

        # Save the results to use in Page 2
        st.session_state.results = results

    # Page 2: Display results
    if st.session_state.results:
        st.subheader("Results:")
        st.json(st.session_state.results)

if __name__ == "__main__":
    main()
