from typing import Optional

import prisma
import prisma.enums
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class UserProfileUpdateResponse(BaseModel):
    """
    The response model for user profile update operations. It confirms the success of the operation and returns the updated user profile.
    """

    success: bool
    updated_user: prisma.models.User


async def update_user(
    userId: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[prisma.enums.UserRole] = None,
) -> UserProfileUpdateResponse:
    """
    Endpoint for updating user profile.

    Args:
        userId (str): The unique identifier of the user whose profile is to be updated.
        username (Optional[str]): The new username for the user. Optional for update.
        email (Optional[str]): The new email address for the user. Optional for update.
        role (Optional[prisma.enums.UserRole]): The role of the user in the system. This can be one of the predefined roles such as CONTENTCREATOR, ADMIN, or INSTITUTION. Optional for update.

    Returns:
        UserProfileUpdateResponse: The response model for user profile update operations. It confirms the success of the operation and returns the updated user profile.

    Raises:
        HTTPException: For non-existent user IDs or conflicts in unique fields like username and email.
    """
    user_data = {}
    if username:
        user_data["username"] = username
    if email:
        user_data["email"] = email
    if role:
        user_data["role"] = role
    try:
        updated_user = await prisma.models.User.prisma().update(
            where={"id": userId}, data=user_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated_user:
        raise HTTPException(status_code=404, detail="prisma.models.User not found.")
    return UserProfileUpdateResponse(success=True, updated_user=updated_user)
