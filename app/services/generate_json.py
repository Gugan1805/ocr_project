import json
import os


class JSONGeneratorService:
    @staticmethod
    def map_json_from_text(result):

            try:
                raw = json.loads(result)

                raw = JSONGeneratorService.remove_empty(raw)

                # Extra safety
                for item in raw.get("items", []):
                    qty = item.get("quantity")
                    amount = item.get("amount")
                    unit_price = item.get("unit_price")

                    if qty is not None and amount is not None and str(qty) == str(amount):
                        item.pop("quantity", None)

                    if qty is not None and unit_price is not None and str(qty) == str(unit_price):
                        item.pop("quantity", None)

                # Convert items to required table format
                table = []

                for item in raw.get("items", []):
                    table.append({
                        "Product Description": item.get("description", ""),
                        "Quantity": item.get("quantity", ""),
                        "Unit Price": item.get("unit_price", ""),
                        "Amount": item.get("amount", "")
                    })

                # Match required response format
                data = {
                    "Invoice Number": raw.get("invoice_number", ""),
                    "Date of Invoice": raw.get("invoice_date", ""),
                    "Total RM": raw.get("total_amount", ""),
                    "Dealer Name": raw.get("vendor_name", ""),
                    "Area": raw.get("area", ""),
                    "table": table,
                    "isInvoice": raw.get("document_type", "").lower() == "invoice"
                }

                return data

            except json.JSONDecodeError:
                raise Exception("AI returned invalid JSON.")

    @staticmethod
    def remove_empty(obj):
        """ Recursively remove empty values from a dictionary or list."""
        if isinstance(obj, dict):
            return {
                k: JSONGeneratorService.remove_empty(v)
                for k, v in obj.items()
                if v not in ("", None, [], {})
            }

        if isinstance(obj, list):
            return [JSONGeneratorService.remove_empty(i) for i in obj if i not in ("", None, [], {})]

        return obj
    
    