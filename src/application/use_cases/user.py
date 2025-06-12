from src.application.dto.user import UserDTO
from src.domain.repositories.abstract_user_repository import AbstractUserRepository
from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.shared.dto.result import ResultDTO


class EnsureUserExistsUseCase:
    def __init__(self, user_repo: AbstractUserRepository):
        self._repo = user_repo

    async def __call__(self, user_dto: UserDTO, *args, **kwds) -> ResultDTO[User]:
        """
        Execute the use case to create a user.
        If the user already exists, it returns the existing user.
        If the user does not exist, it creates a new user.
        """
        user = await self._repo.get_user_by_chat_id(
            user_dto.chat_id
        )  # TODO: Add try-except for error handling
        if user is None:
            created_user = await self._repo.create(
                User(
                    name=user_dto.name,
                    username=user_dto.username,
                    chat_id=user_dto.chat_id,
                    role=UserRole.CLIENT,
                )
            )
            if created_user:
                return ResultDTO.success(created_user)
            return ResultDTO.fail("Failed to create user")

        return ResultDTO.success(user)
