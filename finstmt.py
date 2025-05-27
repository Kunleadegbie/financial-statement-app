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
cash = st.number_input("Cash and Cash Equivalents", min_value=0.0, value=0.0)
inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
receivables = st.number_input("Trade Receivables", min_value=0.0, value=0.0)
fixed_assets = st.number_input("Fixed Assets", min_value=0.0, value=0.0)
payables = st.number_input("Trade Payables", min_value=0.0, value=0.0)
short_term_loans = st.number_input("Short-term Loans", min_value=0.0, value=0.0)
long_term_loans = st.number_input("Long-term Loans", min_value=0.0, value=0.0)
share_capital = st.number_input("Share Capital", min_value=0.0, value=0.0)
retained_earnings = st.number_input("Retained Earnings (Previous Years)", min_value=0.0, value=0.0)

st.subheader("Cash Flow Items")
cash_from_operations = st.number_input("Net Cash from Operating Activities", min_value=0.0, value=0.0)
cash_from_investing = st.number_input("Net Cash from Investing Activities", value=0.0)
cash_from_financing = st.number_input("Net Cash from Financing Activities", value=0.0)

# Generate Button
if st.button("📊 Generate Financial Statements"):

    ## Profit & Loss Statement
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

    ## Balance Sheet
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

    ## Cash Flow Statement
    net_increase_cash = cash_from_operations + cash_from_investing + cash_from_financing
    closing_cash = cash

    cash_flow = pd.DataFrame({
        "Description": ["Net Cash from Operating Activities", "Net Cash from Investing Activities",
                        "Net Cash from Financing Activities", "Net Increase in Cash", "Closing Cash Balance"],
        "Amount": [cash_from_operations, cash_from_investing, cash_from_financing, net_increase_cash, closing_cash]
    })

    ## Financial Ratios
    current_ratio = (cash + receivables + inventory) / (payables + short_term_loans) if (payables + short_term_loans) else np.nan
    quick_ratio = (cash + receivables) / (payables + short_term_loans) if (payables + short_term_loans) else np.nan
    debt_equity_ratio = (short_term_loans + long_term_loans) / total_equity if total_equity else np.nan
    gross_margin = gross_profit / sales if sales else np.nan
    operating_margin = operating_profit / sales if sales else np.nan
    net_margin = profit_after_tax / sales if sales else np.nan
    roe = profit_after_tax / total_equity if total_equity else np.nan

    ratios = pd.DataFrame({
        "Ratio": ["Current Ratio", "Quick Ratio", "Debt to Equity Ratio", "Gross Profit Margin",
                  "Operating Margin", "Net Profit Margin", "Return on Equity (ROE)"],
        "Value": [round(current_ratio, 2), round(quick_ratio, 2), round(debt_equity_ratio, 2),
                  round(gross_margin, 2), round(operating_margin, 2), round(net_margin, 2), round(roe, 2)]
    })

    ## Implications & Recommendations
    implications = []
    recommendations = []

    for index, row in ratios.iterrows():
        ratio_name = row["Ratio"]
        value = row["Value"]

        if np.isnan(value):
            implications.append("Not enough data")
            recommendations.append("Provide missing figures")
        else:
            if ratio_name == "Current Ratio":
                if value < 1:
                    implications.append("Liquidity risk; may struggle to meet short-term obligations")
                    recommendations.append("Improve working capital position")
                elif value > 2:
                    implications.append("Excess idle resources")
                    recommendations.append("Invest excess liquidity or reduce liabilities")
                else:
                    implications.append("Healthy liquidity position")
                    recommendations.append("Maintain balance")

            elif ratio_name == "Quick Ratio":
                if value < 1:
                    implications.append("Weak liquidity")
                    recommendations.append("Boost liquid assets or reduce current liabilities")
                else:
                    implications.append("Good liquidity buffer")
                    recommendations.append("Maintain current level")

            elif ratio_name == "Debt to Equity Ratio":
                if value > 2:
                    implications.append("High financial risk due to excessive leverage")
                    recommendations.append("Reduce debt or increase equity")
                else:
                    implications.append("Acceptable leverage level")
                    recommendations.append("Maintain or optimize capital structure")

            elif ratio_name == "Gross Profit Margin":
                if value < 0.2:
                    implications.append("Low profitability on sales")
                    recommendations.append("Reduce cost of sales or increase selling prices")
                else:
                    implications.append("Good profitability")
                    recommendations.append("Maintain margin levels")

            elif ratio_name == "Operating Margin":
                if value < 0.1:
                    implications.append("Operational inefficiencies")
                    recommendations.append("Control operating expenses")
                else:
                    implications.append("Efficient operations")
                    recommendations.append("Maintain cost control")

            elif ratio_name == "Net Profit Margin":
                if value < 0.05:
                    implications.append("Low profitability")
                    recommendations.append("Increase revenue or reduce total expenses")
                else:
                    implications.append("Healthy bottom-line profitability")
                    recommendations.append("Sustain performance")

            elif ratio_name == "Return on Equity (ROE)":
                if value < 0.1:
                    implications.append("Low return for shareholders")
                    recommendations.append("Improve profitability or optimize equity")
                else:
                    implications.append("Good return for shareholders")
                    recommendations.append("Maintain or enhance ROE")

    ratio_analysis = pd.DataFrame({
        "Ratio": ratios["Ratio"],
        "Value": ratios["Value"],
        "Implication": implications,
        "Recommendation": recommendations
    })

    # 📊 Display Financial Statements
    st.subheader("📑 Profit & Loss Statement")
    st.dataframe(profit_loss)

    st.subheader("📑 Balance Sheet")
    st.dataframe(balance_sheet)

    st.subheader("📑 Cash Flow Statement")
    st.dataframe(cash_flow)

    st.subheader("📊 Financial Ratios & Analysis")
    st.dataframe(ratio_analysis)

    # 📥 Excel Export
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        profit_loss.to_excel(writer, sheet_name="Profit & Loss", index=False)
        balance_sheet.to_excel(writer, sheet_name="Balance Sheet", index=False)
        cash_flow.to_excel(writer, sheet_name="Cash Flow", index=False)
        ratios.to_excel(writer, sheet_name="Ratios", index=False)
        ratio_analysis.to_excel(writer, sheet_name="Recommendations", index=False)
    

    st.download_button(
        label="📥 Download Financial Report (Excel)",
        data=buffer,
        file_name="Financial_Statements_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
