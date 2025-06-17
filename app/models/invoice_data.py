from dataclasses import dataclass

@dataclass
class InvoiceData:
    name: str
    date: str
    amount: str
    invoice_id: str

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "amount": self.amount,
            "invoice_id": self.invoice_id
        }
