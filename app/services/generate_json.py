import json
import os


class JSONGeneratorService:
    @staticmethod
    def map_json_from_text(result):
        """Map extracted text to JSON format."""
        
        try:
        
            data = json.loads(result)
            
            data = JSONGeneratorService.remove_empty(data)

            # Extra safety: prevent amount being copied into quantity
            for item in data.get("items", []):

                qty = item.get("quantity")
                amount = item.get("amount")
                unit_price = item.get("unit_price")

                # Quantity should never equal Amount
                if qty is not None and amount is not None and str(qty) == str(amount):
                    item.pop("quantity", None)

                # Quantity should never equal Unit Price
                if qty is not None and unit_price is not None and str(qty) == str(unit_price):
                    item.pop("quantity", None)

            return data

        except json.JSONDecodeError:
            
            raise Exception("AI returned invalid JSON. Please check the input and try again.")

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
    