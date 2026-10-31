class PaymentReconciliation:
    @staticmethod
    def update_invoice_status(total_amount: float, previously_paid: float, new_payment: float) -> tuple[float, str]:
        new_total_paid = round(previously_paid + new_payment, 2)
        if new_total_paid >= total_amount:
            return new_total_paid, "paid"
        return new_total_paid, "confirmed"
