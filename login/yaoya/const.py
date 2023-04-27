from enum import Enum, auto


class SessionKey(Enum):
    AUTH_API_CLIENT = auto()
    USER_API_CLIENT = auto()
    USER = auto()
    PAGE_ID = auto()
    SESSION_ID = auto()
    USERBOX = auto()

class PageId(Enum):
    PUBLIC_LOGIN = auto()

class UserRole(Enum):
    ADMIN = auto()
    MEMBER = auto()
