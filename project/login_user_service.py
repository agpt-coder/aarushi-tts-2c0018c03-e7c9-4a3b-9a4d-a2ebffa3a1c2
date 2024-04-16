from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Provides feedback on the login attempt, including session information on successful authentication.
    """

    success: bool
    message: str
    session_token: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Endpoint for user login.

    Args:
        email (str): The email address the user is trying to authenticate with.
        password (str): The password provided by the user for authentication purposes.

    Returns:
        UserLoginResponse: Provides feedback on the login attempt, including session information on successful authentication.

    This function looks up the user by email, verifies the password, and if successful,
    generates a session token.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist.",
        )
    if not pwd_context.verify(password, user.hashedPassword):
        return UserLoginResponse(success=False, message="Incorrect password.")
    session_token = "dummy_session_token_for_user_" + user.id
    return UserLoginResponse(
        success=True, message="Login successful.", session_token=session_token
    )
