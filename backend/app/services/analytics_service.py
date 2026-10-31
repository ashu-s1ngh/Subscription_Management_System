class AnalyticsService:
    @staticmethod
    def normalize_to_mrr(price: float, cycle: str) -> float:
        if cycle == "daily":
            return price * 30.0
        elif cycle == "weekly":
            return price * 4.33
        elif cycle == "monthly":
            return price
        elif cycle == "yearly":
            return round(price / 12.0, 2)
        return price
