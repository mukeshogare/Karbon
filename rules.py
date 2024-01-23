# total revenue

import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field

# This is a already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    if "financials" in data:
        # Check if the specified financial_index is within the valid range
        if 0 <= financial_index < len(data["financials"]):
            # Access the financial entry at the specified index
            financial_entry = data["financials"][financial_index]

            # Check if "pnl" key exists in the financial entry
            if "pnl" in financial_entry and "lineItems" in financial_entry["pnl"]:
                # Access the "lineItems" under "pnl"
                line_items = financial_entry["pnl"]["lineItems"]

                # Check if "netRevenue" key exists in line items
                if "netRevenue" in line_items:
                    # Retrieve and return the net revenue value
                    return line_items["netRevenue"]

    # If any required key is missing or the index is invalid, return None
    return None


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the `total_revenue` function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total b              orrowings to total revenue.
    """
    if 'bs' in data and isinstance(data['bs'], list) and financial_index < len(data['bs']):

    
        long_term_borrowings = sum(data['bs'][financial_index]['long_term_borrowings'])
        short_term_borrowings = sum(data['bs'][financial_index]['short_term_borrowings'])

        # Calculate total revenue using the total_revenue function
        total_rev = total_revenue(data, financial_index)

        # Calculate the ratio of total borrowings to total revenue
        if total_rev != 0:
            ratio = (long_term_borrowings + short_term_borrowings) / total_rev
            return ratio
        else:
            # Avoid division by zero, return None or raise an exception as appropriate
            return None
        
    else :
        return 0.0


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the `iscr` function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)

    if iscr_value >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the `total_revenue` function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    total_rev = total_revenue(data, financial_index)  # Assuming you have a total_revenue function

    if total_rev is not None and total_rev >= 50000000:  # 50 million
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    # Retrieve relevant financial data
    profit_before_interest_tax_deprec_list = data.get("profit_before_interest_tax_deprec", [])
    interest_expenses_list = data.get("interest_expenses", [])

    # Check if financial_index is within the valid range
    if 0 <= financial_index < min(len(profit_before_interest_tax_deprec_list), len(interest_expenses_list)):
        profit_before_interest_tax_deprec = profit_before_interest_tax_deprec_list[financial_index]
        interest_expenses = interest_expenses_list[financial_index]

        # Calculate ISCR
        iscr_value = (profit_before_interest_tax_deprec + 1) / (interest_expenses + 1)

        return iscr_value
    else:
        # Handle the case when financial_index is out of range
        return 0.0  # or any default value you prefer


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the `total_borrowing`
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
     # Check if 'total_revenue' key is present in the dictionary
    if 'total_revenue' in data and isinstance(data['total_revenue'], list) and financial_index < len(data['total_revenue']):
        total_borrowings = total_borrowing(data, financial_index)
        total_revenue = data['total_revenue'][financial_index]

        # Calculate the ratio of total borrowings to total revenue
        ratio = total_borrowings / total_revenue

        # Determine the flag color based on the ratio
        if ratio <= 0.25:
            return FLAGS.GREEN
        else:
            return FLAGS.AMBER
    else:
        # Handle the case when 'total_revenue' key is not present or financial_index is out of range
        return FLAGS.AMBER  # or any default value you prefer

