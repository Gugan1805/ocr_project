from openai import OpenAI

from app.core.config import settings
from app.services.file_converter import FileConverter


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_document(self, bytes_data: bytes, prompt: str, extension: str):
        file_data = FileConverter.prepare_file(bytes_data, extension)
        
        images = file_data["images"]
        page_count = file_data["page_count"]

        content = [
            {
                "type": "input_text",
                "text": prompt,
            }
        ]

        for encoded in images:
            content.append({
                "type": "input_image",
                "image_url": f"data:image/png;base64,{encoded}",
            })

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )

        return {
            "text": response.output_text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "page_count" : page_count
        }
    
    def price_calculation(self, usage):
        input_cost = (usage["input_tokens"] / 1_000_000) * 0.20
        output_cost = (usage["output_tokens"] / 1_000_000) * 1.20

        total_cost = input_cost + output_cost

        return {
            "input": {
                "token": usage["input_tokens"],
                "cost": input_cost
            },
            "output": {
                "token": usage["output_tokens"],
                "cost": output_cost
            },
            "total": {
                "tokens": usage["total_tokens"],
                "cost": total_cost
            }
        }