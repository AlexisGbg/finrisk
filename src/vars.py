from enum import Enum

class INCOME_STMT_KPI(Enum):
    REVENUE = "Total Revenue"
    COGS = "Operating Expense"
    GROSS_PROFIT = "Gross Profit"
    EBITDA = "EBITDA"
    INTEREST_EXPENSE = "Interest Expense"

class BALANCE_SHEET_KPI(Enum):
    TOTAL_DEPT = "Total Debt"
    CASH = "Cash And Cash Equivalents"
