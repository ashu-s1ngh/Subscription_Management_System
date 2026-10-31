from datetime import date, timedelta
from app.services.billing_engine import BillingEngine

class InvoiceGenerator:
    @staticmethod
    def generate_next_billing_period(start_date: date, cycle: str) -> tuple[date, date]:
        if cycle == "daily":
            return start_date, start_date + timedelta(days=1)
        elif cycle == "weekly":
            return start_date, start_date + timedelta(weeks=1)
        elif cycle == "monthly":
            return start_date, start_date + timedelta(days=30)
        elif cycle == "yearly":
            return start_date, start_date + timedelta(days=365)
        return start_date, start_date + timedelta(days=30)
