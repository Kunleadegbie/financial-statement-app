import streamlit as st
import pandas as pd
import numpy as np
import io

# Streamlit page setup
st.set_page_config(page_title="Automated Financial Statement Generator", layout="wide")

st.title("📊 Automated Financial Statement Generator")
st.write("Prepare Balance Sheet, Profit & Loss, and Cash Flow Statements with financial ratio analysis instantly.")
st.markdown("---")

# Company Details
st.sidebar.header("📌 Company Information")
company_name = st.sidebar.text_input("Company Name", value="Your Company Ltd.")
reporting_period = st.sidebar.text_input("Reporting Period", value="For the year ended 31st December 2024")
prepared_by = st.sidebar.text_input("Prepared by", value="Chumcred Limited")

# Financial Data Inputs
st.header("📥 Input Financial Data")

st.subheader("Profit & Loss Items")
sales = st.number_input("Revenue (Sales)", min_value=0.0, value=0.0)
cost_of_sales = st.number_input("Cost of Sales", min_value=0.0, value=0.0)
operating_expenses = st.number_input("Operating Expenses", min_value=0.0, value=0.0)
interest_expense = st.number_input("Interest Expense", min_value=0.0, value=0.0)
other_income = st.number_input("Other Income", min_value=0.0, value=0.0)
tax_expense = st.number_input("Tax Expense", min_value=0.0, value=0.0)

st.subheader("Balance Sheet Items")
# Assets
cash = st.number_input("Cash and Cash Equivalents", min_value=0.0, value=0.0)
inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
receivables = st.number_input("Trade Receivables", min_value=0.0, value=0.0)
fixed_assets = st.number_input("Fixed Assets", min_value=0.0, value=0.0)
# Liabilities
payables = st.number_input("Trade Payables", min_value=0.0, value=0.0)
short_term_loans = st.number_input("Short-term Loans", min_value=0.0, value=0.0)
long_term_loans = st.number_input("Long-term Loans", min_value=0.0, value=0.0)
# Equity
share_capital = st.number_input("Share Capital", min_value=0.0, value=0.0)
retained_earnings = st.number_input("Retained Earnings (Previous Years)", min_value=0.0, value=0.0)

st.subheader("Cash Flow Items")
cash_from_operations = st.number_input("Net Cash from Operating Activities", min_value=0.0, value=0.0)
cash_from_investing = st.number_input("Net Cash from Investing Activities", value=0.0)
cash_from_financing = st.number_input("Net Cash from Financing Activities", value=0.0)

# Action button to generate reports
if st.button("📊 Generate Financial Statements"):

    # Profit & Loss Statement
    gross_profit = sales - cost_of_sales
    operating_profit = gross_profit - operating_expenses + other_income
    profit_before_tax = operating_profit - interest_expense
    profit_after_tax = profit_before_tax - tax_expense
    retained_earnings_current = profit_after_tax

    profit_loss = pd.DataFrame({
        "Description": ["Revenue", "Cost of Sales", "Gross Profit", "Operating Expenses", "Other Income",
                        "Operating Profit", "Interest Expense", "Profit Before Tax", "Tax Expense", "Profit After Tax"],
        "Amount": [sales, -cost_of_sales, gross_profit, -operating_expenses, other_income, operating_profit,
                   -interest_expense, profit_before_tax, -tax_expense, profit_after_tax]
    })

    # Balance Sheet
    total_assets = cash + inventory + receivables + fixed_assets
    total_liabilities = payables + short_term_loans + long_term_loans
    total_equity = share_capital + retained_earnings + retained_earnings_current
    balance_sheet = pd.DataFrame({
        "Description": ["Assets", "Cash and Cash Equivalents", "Inventory", "Trade Receivables", "Fixed Assets",
                        "Total Assets", "", "Liabilities", "Trade Payables", "Short-term Loans", "Long-term Loans",
                        "Total Liabilities", "", "Equity", "Share Capital", "Retained Earnings (Previous Years)",
                        "Retained Earnings (Current Year)", "Total Equity"],
        "Amount": [None, cash, inventory, receivables, fixed_assets, total_assets, None,
                   None, payables, short_term_loans, long_term_loans, total_liabilities, None,
                   None, share_capital, retained_earnings, retained_earnings_current, total_equity]
    })

    # Cash Flow Statement
    net_increase_cash = cash_from_operations + cash_from_investing + cash_from_financing
    closing_cash = cash

    cash_flow = pd.DataFrame({
        "Description": ["Net Cash from Operating Activities", "Net Cash from Investing Activities",
                        "Net Cash from Financing Activities", "Net Increase in Cash", "Closing Cash Balance"],
        "Amount": [cash_from_operations, cash_from_investing, cash_from_financing, net_increase_cash, closing_cash]
    })

    # Financial Ratios
    ratios = {
        "Current Ratio": round((cash + receivables + inventory) / (payables + short_term_loans)
                               if (payables + short_term_loans) else np.nan, 2),
        "Quick Ratio": round((cash + receivables) / (payables + short_term_loans)
                               if (payables + short_term_loans) else np.nan, 2),
        "Debt to Equity Ratio": round((short_term_loans + long_term_loans) / total_equity if total_equity else np.nan, 2),
        "Gross Profit Margin": round(gross_profit / sales if sales else np.nan, 2),
        "Operating Margin": round(operating_profit / sales if sales else np.nan, 2),
        "Net Profit Margin": round(profit_after_tax / sales if sales else np.nan, 2),
        "Return on Equity (ROE)": round(profit_after_tax / total_equity if total_equity else np.nan, 2)
    }

    # New: Add Analysis, Implications, Recommendations
    ratio_analysis = {
        "Current Ratio": ("Indicates liquidity", "Company can meet short-term obligations", "Maintain or improve working capital management"),
        "Quick Ratio": ("Measures immediate liquidity", "Ability to settle short-term debts without selling inventory", "Improve receivables collection"),
        "Debt to Equity Ratio": ("Assesses financial leverage", "Higher ratio implies more debt risk", "Balance debt-equity mix prudently"),
        "Gross Profit Margin": ("Shows profitability from core operations", "Higher margin means effective cost control", "Maintain or improve gross margins"),
        "Operating Margin": ("Reflects operational efficiency", "Higher margin indicates good cost control", "Monitor operating expenses"),
        "Net Profit Margin": ("Shows overall profitability", "Higher ratio indicates good bottom line", "Enhance operational and financial efficiency"),
        "Return on Equity (ROE)": ("Measures return to shareholders", "Higher ROE is favorable", "Sustain profitability and equity base")
    }

    ratios_df = pd.DataFrame([
        {
            "Ratio": ratio,
            "Value": value,
            "Analysis": ratio_analysis[ratio][0],
            "Implications": ratio_analysis[ratio][1],
            "Recommendations": ratio_analysis[ratio][2]
        }
        for ratio, value in ratios.items()
    ])

    st.success("✅ Financial Statements Generated")

    # Display on Screen
    st.subheader("📄 Balance Sheet")
    st.dataframe(balance_sheet)

    st.subheader("📄 Profit & Loss Statement")
    st.dataframe(profit_loss)

    st.subheader("📄 Cash Flow Statement")
    st.dataframe(cash_flow)

    st.subheader("📊 Financial Ratios")
    st.dataframe(ratios_df)

    # Excel Download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Balance Sheet
        balance_sheet.to_excel(writer, index=False, sheet_name="Balance Sheet", startrow=4)
        ws = writer.sheets["Balance Sheet"]
        ws.write("A1", f"{company_name} - Balance Sheet")
        ws.write("A2", reporting_period)
        ws.write("A3", f"Prepared by: {prepared_by}")

        # Profit & Loss
        profit_loss.to_excel(writer, index=False, sheet_name="Profit & Loss", startrow=4)
        ws = writer.sheets["Profit & Loss"]
        ws.write("A1", f"{company_name} - Profit & Loss")
        ws.write("A2", reporting_period)
        ws.write("A3", f"Prepared by: {prepared_by}")

        # Cash Flow
        cash_flow.to_excel(writer, index=False, sheet_name="Cash Flow", startrow=4)
        ws = writer.sheets["Cash Flow"]
        ws.write("A1", f"{company_name} - Cash Flow")
        ws.write("A2", reporting_period)
        ws.write("A3", f"Prepared by: {prepared_by}")

        # Financial Ratios
        ratios_df.to_excel(writer, index=False, sheet_name="Financial Ratios", startrow=4)
        ws = writer.sheets["Financial Ratios"]
        ws.write("A1", f"{company_name} - Financial Ratios")
        ws.write("A2", reporting_period)
        ws.write("A3", f"Prepared by: {prepared_by}")

    st.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name="financial_statements.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
