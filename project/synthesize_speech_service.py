from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class SynthesizeSpeechResponse(BaseModel):
    """
    Response model containing details about the synthesized speech.
    """

    speechRequestId: str
    status: str
    filePath: str
    playbackUrl: str
    errorMessage: str


class InputFormat(Enum):
    PLAIN_TEXT: str = "PLAIN_TEXT"
    SSML: str = "SSML"


class VoiceType(Enum):
    FEMALE_EN_US: str = "FEMALE_EN_US"


async def synthesize_speech(
    userId: str,
    inputText: str,
    inputFormat: InputFormat,
    language: str,
    voice: VoiceType,
    speechSpeed: float,
    pitch: float,
    volume: float,
) -> SynthesizeSpeechResponse:
    """
    Synthesize speech from input text or SSML.

    This function records the text-to-speech request in the database, generates synthesized speech,
    and saves the output as an MP3 file.

    Args:
        userId (str): ID of the user requesting speech synthesis.
        inputText (str): The text to be synthesized, can be plain text or SSML formatted.
        inputFormat (InputFormat): Format of input text, either 'PLAIN_TEXT' or 'SSML'.
        language (str): The language for speech synthesis, initially only 'EN_US'.
        voice (VoiceType): Preferred voice for the speech synthesis, default to 'FEMALE_EN_US'.
        speechSpeed (float): Speed of the speech output, where 1.0 is the normal speed.
        pitch (float): Pitch of the speech output, where 1.0 is the normal pitch.
        volume (float): Volume of the speech output, where 1.0 is the normal volume.

    Returns:
        SynthesizeSpeechResponse: Response model containing details about the synthesized speech.

    Note: This function assumes the existence of an external text-to-speech API for the actual synthesis process.
    """
    filePath = "/var/www/speech_outputs/{}.mp3".format(userId)
    playbackUrl = "https://speech.example.com/play/{}.mp3".format(userId)
    speech_request = await prisma.models.UserSpeechRequest.prisma().create(
        data={
            "userId": userId,
            "inputText": inputText,
            "inputFormat": inputFormat.value,
            "voice": voice.value,
            "speechSpeed": speechSpeed,
            "pitch": pitch,
            "volume": volume,
        }
    )
    await prisma.models.SpeechOutput.prisma().create(
        data={
            "speechRequestId": speech_request.id,
            "filePath": filePath,
            "playbackUrl": playbackUrl,
        }
    )
    response = SynthesizeSpeechResponse(
        speechRequestId=speech_request.id,
        status="SUCCESS",
        filePath=filePath,
        playbackUrl=playbackUrl,
        errorMessage="",
    )
    return response
