import fitz
import base64


class FileConverter:
    @staticmethod
    def convert_pdf_to_images(bytes_data: bytes):
        """Convert PDF pages to Base64 encoded PNG images."""
        images = []
        pdf = fitz.open(stream=bytes_data, filetype="pdf")

        for page in pdf:
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")

            # Encode the generated image, not the PDF
            encoded = base64.b64encode(image_bytes).decode("utf-8")
            images.append(encoded)

        pdf.close()
        return images

    @staticmethod
    def prepare_file(bytes_data: bytes, extension: str):
        """
        Prepare file for processing based on its extension.

        Args:
            bytes_data: File content in bytes.
            extension: File extension (e.g. ".pdf").
        """

        if extension == ".pdf":
            print("PDF detected")
            return FileConverter.convert_pdf_to_images(bytes_data)

        elif extension in [".png", ".jpg", ".jpeg"]:
            print("Image detected")
            return [base64.b64encode(bytes_data).decode("utf-8")]

        else:
            raise ValueError(f"Unsupported file type: {extension}")