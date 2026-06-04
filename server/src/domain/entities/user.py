from bcrypt import gensalt, hashpw

class User:
    def __init__(self, username: str, password_hash: bytes, role:str):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    async def create(username: str, password: str, role: str):
        password_hash = hashpw(password.encode("utf-8"), gensalt())
        return User(username, password_hash, role)
