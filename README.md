# OCR Project

## Overview

This project is a FastAPI application for extracting structured JSON data from uploaded document images or files using an OCR and AI-assisted extraction service.

The API accepts a file upload and returns parsed JSON with fields such as:
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
- items

## UI / Usage Format

Use the `/ocr/extract` endpoint with a `POST` request and a file upload using `multipart/form-data`.

Example request format:

- Endpoint: `POST /ocr/extract`
- Content type: `multipart/form-data`
- Field name: `file`
- Value: choose the uploaded document file

Example response structure:

```
{
  "response": {
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
  },
  "message": "Successfully extracted and saved JSON data."
}
```

## Notes for UI design

- Display a clear upload area labeled `Upload Document`.
- Show supported document types: Invoice, Sales report, Sales analysis report.
- Use a progress indicator while the file is processed.
- Render the returned JSON in a readable format after extraction.
- Provide success and error messages clearly.

## How it works

1. Upload a document file.
2. The API sends the file bytes to the AI extraction service.
3. The AI returns extracted data as text.
4. The JSON generator service maps the AI response to JSON and saves it.
5. The API returns the final JSON response.
