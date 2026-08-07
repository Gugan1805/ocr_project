
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

Vendor information extraction:

vendor_name
- Extract from the company name/header at the top of the document.

vendor_address
- Extract the full address located below the vendor/company name.
- Preserve the address exactly as printed.
- Do not omit address lines.
- Do not confuse customer address with vendor address.

vendor_phone
- Extract phone numbers near the vendor information.

vendor_email
- Extract email addresses near the vendor information.

vendor_registration_number
- Extract company registration numbers such as:
  - (491923-U)
  - Registration No
  - SSM No
  - Company No
  
Top-level fields should only be included if present:
- document_type
- invoice_number
- invoice_date
- vendor_name
- vendor_address
- vendor_phone
- vendor_email
- vendor_registration_number
- customer_name
- customer_address
- subtotal
- tax
- total_amount
- currency
- total_quantity

Invoice Total Extraction Rules

For invoice documents:

total_amount
- Extract the final payable amount printed on the invoice.
- It may appear beside labels such as:
  - TOTAL
  - GRAND TOTAL
  - NET TOTAL
  - TOTAL AMOUNT
  - AMOUNT DUE
  - BALANCE DUE
- If there is only one final total printed at the bottom of the invoice, use that value.
- NEVER use the line item amount if a final invoice total exists.
- NEVER calculate the total yourself.
- Preserve the value exactly as printed.

Footer Totals

Also extract any totals shown in the footer of the document.

Possible labels include:
- Total
- Grand Total
- Net Total
- Total Amount
- Amount Due
- Balance Due

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
    
    json_data = service_generate.map_json_from_text(response["text"])
    usage_data = service_ai.price_calculation(response['usage'])
    

    return {
        "status": True,
        "message": "1 out of 1 files processed",
        "data": {
            file.filename: {
                "status": True,
                "message": "File processed successfully",
                "data": json_data,
                "status_code": 200,
                "isInvoice": json_data["isInvoice"],
                "invoice_number": json_data["Invoice Number"],
                "processing_time": "",
                "number_of_pages": ""
            }
        },
        "page_count": response['page_count'],
        'pricing' : usage_data
    }