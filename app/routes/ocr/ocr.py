
from fastapi import APIRouter, File, UploadFile
import os

from app.services.generate_json import JSONGeneratorService
from app.services.openai import OpenAIService


router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)


@router.post("/extract")
async def extract(
    file: UploadFile = File(...),
):
    
    service_ai = OpenAIService()
    service_generate = JSONGeneratorService()
    
    file_name = file.filename
    extension = os.path.splitext(file_name)[1].lower()
    
    bytes_data = await file.read()
    
    response = service_ai.extract_document(
        bytes_data=bytes_data,
        prompt="""
                Extract all information from this document.

                The document may be:
                - Invoice
                - Sales report
                - Sales analysis report

                Return ONLY valid JSON.

                Rules:

                1. ONLY include fields that actually exist in the document.
                2. DO NOT create empty fields.
                3. If a field does not exist, OMIT it completely.
                4. Extract every line item exactly as shown.
                5. Never skip rows.
                6. Never merge rows.
                7. Never guess values.
                8. Never calculate missing values.
                9. Preserve the document values exactly.
                10. Return JSON only.
                11. No markdown.
                12. No explanation.

                Field Mapping Rules (VERY IMPORTANT)

                Each field MUST come ONLY from its corresponding column.

                quantity
                - ONLY from a column named Quantity, Qty, Qty Ordered, Ordered Qty.
                - NEVER use Amount.
                - NEVER use Total.
                - NEVER use Unit Price.
                - NEVER use Price.
                - NEVER use Balance.
                - If there is no quantity column, DO NOT include quantity.

                unit_price
                - ONLY from Unit Price, Price, Rate , Gross Sales.
                - NEVER use Amount.
                - NEVER use Total.
                - NEVER use Quantity.

                amount
                - ONLY from Amount, Total, Line Total, Net Amount , Net Sales.
                - NEVER use Quantity.
                - NEVER use Unit Price.

                code
                - ONLY from Item Code, Product Code, SKU , Stock.

                description
                - ONLY from Description, Desc, Item Description, Product Description, Item Name, Product Name.
                - If the document contains a column named Desc, map it to description.
                - Preserve all line breaks inside the description.

                Top-level fields should only be included if present:
                - document_type
                - invoice_number
                - invoice_date
                - vendor_name
                - customer_name
                - subtotal
                - tax
                - total_amount
                - currency
                - total_quantity

                if total_quantity is present, change its name to total_amount.

                subtotal
                - ONLY from the Quantity column of the Sub Total or Grand Total row.

                total_amount
                - ONLY from the Net Sales column of the Sub Total or Grand Total row.

                Never use Quantity as subtotal.
                Never use Discount as subtotal.
                Never use Gross Sales as total_amount.
                Never use Quantity as total_amount.

                Example:

                {
                "document_type": "Invoice",
                "invoice_number": "INV1001",
                "vendor_name": "ABC Sdn Bhd",
                "invoice_date": "2025-02-01",
                "items": [
                    {
                    "code": "P100",
                    "description": "Rice",
                    "unit_price": "12.50",
                    "amount": "125.00"
                    },
                    {
                    "description": "Oil",
                    "quantity": "5",
                    "amount": "75.00"
                    }
                ],
                "total_amount": "200.00"
                }

                Notice:
                - quantity is omitted if not present.
                - code is omitted if not present.
                - subtotal is omitted if not present.
                - tax is omitted if not present.
                - Never output empty strings.

                For every row:

                - code comes from Item Code
                - description comes from Desc
                - quantity comes from Qty
                - unit_price comes from Unit Price

                Never omit description if the Desc column exists.
                Every item in the items array must contain the description field.
        """,
        extension = extension,
    )
    
    
    json_data = service_generate.map_json_from_text(response)
    
    return {
        "response": json_data,
        "message": "Successfully extracted and saved JSON data.",
    }