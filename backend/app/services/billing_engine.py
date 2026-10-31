class BillingEngine:
    @staticmethod
    def calculate_item_price(base_price: float, variant_price_adjustment: float = 0.0) -> float:
        return round(base_price + variant_price_adjustment, 2)

    @staticmethod
    def calculate_subtotal(items: list[dict]) -> float:
        return round(sum(item["unit_price"] * item["quantity"] for item in items), 2)

    @staticmethod
    def apply_discount(subtotal: float, discount: dict, total_qty: int = 1) -> float:
        if not discount or not discount.get("is_active"):
            return 0.0

        if subtotal < discount.get("min_purchase", 0):
            return 0.0

        if total_qty < discount.get("min_quantity", 0):
            return 0.0

        if discount["type"] == "percentage":
            return round(subtotal * (discount["value"] / 100.0), 2)
        elif discount["type"] == "fixed":
            return round(min(discount["value"], subtotal), 2)
        return 0.0

    @staticmethod
    def calculate_tax(taxable_amount: float, tax_rate_percent: float = 18.0) -> float:
        return round(taxable_amount * (tax_rate_percent / 100.0), 2)

    @classmethod
    def compute_invoice_totals(cls, items: list[dict], discount: dict = None, tax_rate: float = 18.0) -> dict:
        subtotal = cls.calculate_subtotal(items)
        total_qty = sum(item.get("quantity", 1) for item in items)
        disc_amount = cls.apply_discount(subtotal, discount, total_qty) if discount else 0.0
        taxable_base = max(0.0, subtotal - disc_amount)
        tax_amount = cls.calculate_tax(taxable_base, tax_rate)
        total = round(taxable_base + tax_amount, 2)

        return {
            "subtotal": subtotal,
            "discount": disc_amount,
            "tax": tax_amount,
            "total_amount": total
        }
