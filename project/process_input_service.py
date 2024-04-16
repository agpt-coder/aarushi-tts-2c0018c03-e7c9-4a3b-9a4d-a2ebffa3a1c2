from typing import Optional

from pydantic import BaseModel


class ProcessTextOutput(BaseModel):
    """
    Model for the output of the text processing. Includes status of the validation and potentially sanitized or transformed text.
    """

    success: bool
    message: str
    processed_text: Optional[str] = None
    request_id: Optional[str] = None


def process_input(
    id: Optional[str],
    text: str,
    format: str,
    language: Optional[str] = None,
    accent: Optional[str] = None,
) -> ProcessTextOutput:
    """
    Process and validate input text or SSML.

    Args:
        id (Optional[str]): Unique identifier for the synthesis request, useful for tracing and logs.
        text (str): Input text to be processed and validated for synthesis. This could be plain text or SSML formatted string.
        format (str): Format of the input text, indicating whether it's plain text or SSML.
        language (Optional[str]): Optional language code for the input text. Defaults to English (en) if not specified.
        accent (Optional[str]): Optional accent code for the speech synthesis. Defaults to American accent if not specified.

    Returns:
        ProcessTextOutput: Model for the output of the text processing. Includes status of the validation and potentially sanitized or transformed text.

    This function assumes basic validation rules:
    - SSML must be well-formed XML.
    - For plain text, ensure it is not empty and does not contain SSML tags.
    """
    if format not in ["PLAIN_TEXT", "SSML"]:
        return ProcessTextOutput(
            success=False, message="Invalid format specified.", request_id=id
        )
    if language is not None and language != "en":
        return ProcessTextOutput(
            success=False,
            message="Unsupported language. Currently only 'en' is supported.",
            request_id=id,
        )
    if accent is not None and accent not in ["American", "British"]:
        return ProcessTextOutput(
            success=False,
            message="Unsupported accent. Currently only 'American' is supported.",
            request_id=id,
        )
    processed_text = None
    if format == "PLAIN_TEXT":
        if not text.strip():
            return ProcessTextOutput(
                success=False, message="Text is empty.", request_id=id
            )
        processed_text = text.strip()
    elif format == "SSML":
        if "<speak>" not in text or "</speak>" not in text:
            return ProcessTextOutput(
                success=False, message="Invalid SSML content.", request_id=id
            )
        processed_text = text
    return ProcessTextOutput(
        success=True,
        message="Text processed successfully.",
        processed_text=processed_text,
        request_id=id,
    )
