import fitz
import base64


class FileConverter:

    @staticmethod
    def convert_pdf_to_images(bytes_data: bytes):
        """Convert PDF pages to Base64 encoded PNG images."""

        images = []
        pdf = fitz.open(stream=bytes_data, filetype="pdf")

        page_count = len(pdf)

        for page in pdf:
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")

            encoded = base64.b64encode(image_bytes).decode("utf-8")
            images.append(encoded)

        pdf.close()

        return {
            "images": images,
            "page_count": page_count
        }

    @staticmethod
    def prepare_file(bytes_data: bytes, extension: str):
        """
        Prepare file for processing based on its extension.
        """

        extension = extension.lower()

        if extension == ".pdf":
            print("PDF detected")

            return FileConverter.convert_pdf_to_images(bytes_data)

        elif extension in [".png", ".jpg", ".jpeg"]:
            print("Image detected")

            return {
                "images": [
                    base64.b64encode(bytes_data).decode("utf-8")
                ],
                "page_count": 1
            }

        else:
            raise ValueError(f"Unsupported file type: {extension}")