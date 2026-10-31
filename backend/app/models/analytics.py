from pydantic import BaseModel
from typing import Dict, List

class AnalyticsSummary(BaseModel):
    mrr: float
    total_revenue: float
    outstanding_balance: float
    active_subscriptions: int
    total_customers: int
    overdue_invoices_count: int
    subscriptions_by_status: Dict[str, int]
