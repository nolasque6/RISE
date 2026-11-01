import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def analyze_scanned_document(
    file_bytes: bytes,
    mime_type: str
) -> str:

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=file_bytes,
                mime_type=mime_type,
            ),
            """
            Read this scanned document carefully.

            Extract all readable text from the document.
            Preserve the structure and important information where possible.
            Do not invent information that is not visible in the document.

            Return only the extracted document content.
            """
        ],
    )

    return response.text