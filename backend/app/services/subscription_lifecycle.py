class SubscriptionLifecycle:
    ALLOWED_TRANSITIONS = {
        "draft": ["quotation", "confirmed"],
        "quotation": ["confirmed", "closed"],
        "confirmed": ["active", "closed"],
        "active": ["paused", "closed"],
        "paused": ["active", "closed"],
        "closed": []
    }

    @classmethod
    def can_transition(cls, current_status: str, next_status: str) -> bool:
        return next_status in cls.ALLOWED_TRANSITIONS.get(current_status, [])
