from bcrypt import gensalt, hashpw


class User:
    def __init__(self, user_id: int | None, username: str, password_hash: bytes, role: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @property
    def user_id(self) -> int | None:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int | None):
        if value is None:
            self.__user_id = value
            return
        if not isinstance(value, int):
            raise TypeError("user_id must be an int")
        if value <= 0:
            raise ValueError("user_id must be positive")
        self.__user_id = value

    @staticmethod
    async def create(username: str, password: str, role: str):
        password_hash = hashpw(password.encode("utf-8"), gensalt())
        return User(None, username, password_hash, role)
