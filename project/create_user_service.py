from enum import Enum

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Confirms the successful creation of a new user account without exposing sensitive information.
    """

    user_id: str
    username: str
    email: str
    role: prisma.enums.UserRole
    message: str


class UserRole(Enum):
    CONTENTCREATOR: str = "CONTENTCREATOR"
    ADMIN: str = "ADMIN"
    INSTITUTION: str = "INSTITUTION"


async def create_user(
    username: str, email: str, password: str, role: prisma.enums.UserRole
) -> UserRegistrationResponse:
    """
    Endpoint for user registration.

    This function creates a new user in the database with all necessary details including a hashed password.
    It leverages the Prisma client to interact with the database and bcrypt for password hashing.

    Args:
    username (str): Desired username for the new account. Must be unique across all users.
    email (str): Email address for the new account. Used for account verification and communication.
    password (str): Password for the new account. This will be hashed for storage.
    role (prisma.enums.UserRole): The role of the user in the system, determining access levels.

    Returns:
    UserRegistrationResponse: Confirms the successful creation of a new user account without exposing sensitive information,
    including the user_id, username, email, role, and a success message.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    created_user = await prisma.models.User.prisma().create(
        data={
            "username": username,
            "email": email,
            "hashedPassword": hashed_password,
            "role": role,
        }
    )
    return UserRegistrationResponse(
        user_id=created_user.id,
        username=created_user.username,
        email=created_user.email,
        role=created_user.role,
        message=f"User {username} successfully created.",
    )
