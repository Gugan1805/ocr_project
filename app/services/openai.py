from openai import OpenAI

from app.core.config import settings
from app.services.file_converter import FileConverter


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_document(self, bytes_data: bytes, prompt: str, extension: str):
        images = FileConverter.prepare_file(bytes_data, extension)

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

        return response.output_text
    
    
