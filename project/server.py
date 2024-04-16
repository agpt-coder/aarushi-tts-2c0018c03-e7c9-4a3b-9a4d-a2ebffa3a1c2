import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.create_user_service
import project.login_user_service
import project.process_input_service
import project.synthesize_speech_service
import project.update_user_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-tts-2",
    lifespan=lifespan,
    description="Based on the information gathered, the project involves creating a feature or API endpoint to convert input text into natural-sounding speech audio, primarily for educational materials. Key requirements and considerations include:\n\n1. **Audio Output Format:** The output should be available in MP3 format, ensuring broad compatibility.\n\n2. **Language and Accent Support:** The speech synthesis must support English with an American accent, aiming for broad accessibility and ease of understanding.\n\n3. **Voice Characteristics:** A female voice is preferred due to its clear and soothing characteristics, suitable for most listening contexts.\n\n4. **Customization Capabilities:** Users need the ability to control speech synthesis parameters, including speech speed, pitch, and volume. This customization facilitates tailored audio outputs that cater to diverse needs and preferences.\n\n5. **Input Text Formats:** The system should accept both plain text and SSML (Speech Synthesis Markup Language) inputs. Plain text offers straightforward usability, while SSML provides nuanced control over the speech synthesis process, enabling richer and more expressive audio outputs.\n\n6. **Best Practices for API Design:** Implementing this text-to-speech (TTS) feature as a REST API involves adhering to best practices such as supporting multiple audio formats, ensuring scalability, utilizing caching mechanisms, securing API access and data transmission, imposing rate limits, offering customization options, promoting accessibility and internationalization, providing comprehensive documentation, and setting up monitoring and feedback mechanisms.\n\n**Tech Stack:** The recommended tech stack includes Python for programming, FastAPI for the API framework given its asynchronous capabilities and ease of use for creating RESTful APIs, PostgreSQL for the database due to its reliability and performance, and Prisma as the ORM to facilitate easy and secure database operations within a Python and FastAPI environment.",
)


@app.post(
    "/text/process", response_model=project.process_input_service.ProcessTextOutput
)
async def api_post_process_input(
    id: Optional[str],
    text: str,
    format: str,
    language: Optional[str],
    accent: Optional[str],
) -> project.process_input_service.ProcessTextOutput | Response:
    """
    Process and validate input text or SSML.
    """
    try:
        res = project.process_input_service.process_input(
            id, text, format, language, accent
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/speech/synthesize",
    response_model=project.synthesize_speech_service.SynthesizeSpeechResponse,
)
async def api_post_synthesize_speech(
    userId: str,
    inputText: str,
    inputFormat: prisma.enums.InputFormat,
    language: str,
    voice: prisma.enums.VoiceType,
    speechSpeed: float,
    pitch: float,
    volume: float,
) -> project.synthesize_speech_service.SynthesizeSpeechResponse | Response:
    """
    Synthesize speech from input text or SSML.
    """
    try:
        res = await project.synthesize_speech_service.synthesize_speech(
            userId, inputText, inputFormat, language, voice, speechSpeed, pitch, volume
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Endpoint for user login.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register",
    response_model=project.create_user_service.UserRegistrationResponse,
)
async def api_post_create_user(
    username: str, email: str, password: str, role: prisma.enums.UserRole
) -> project.create_user_service.UserRegistrationResponse | Response:
    """
    Endpoint for user registration.
    """
    try:
        res = await project.create_user_service.create_user(
            username, email, password, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/user/{userId}",
    response_model=project.update_user_service.UserProfileUpdateResponse,
)
async def api_patch_update_user(
    username: Optional[str],
    userId: str,
    email: Optional[str],
    role: Optional[prisma.enums.UserRole],
) -> project.update_user_service.UserProfileUpdateResponse | Response:
    """
    Endpoint for updating user profile.
    """
    try:
        res = await project.update_user_service.update_user(
            username, userId, email, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
