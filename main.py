from mcp.server.fastmcp import FastMCP
from typing import List

# In-memory mock database with 20 leave days to start
employee_leaves = {
    "Ankush": {"balance": 18, "history": ["2025-04-23", "2025-01-07"]},
    "Bineet": {"balance": 20, "history": []}
}

# Create MCP server
mcp = FastMCP("LeaveManager")

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_name: str) -> str:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_name)
    if data:
        return f"{employee_name} has {data['balance']} leave days remaining."
    return "Employee ID not found."

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_name: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_name not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_name]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_name]["balance"] -= requested_days
    employee_leaves[employee_name]["history"].extend(leave_dates)

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_name]['balance']}."


# Resource: Leave history
@mcp.tool()
def get_leave_history(employee_name: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_name)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_name}: {history}"
    return "Employee ID not found."

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

