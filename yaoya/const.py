from enum import Enum, auto

class PageId(Enum):
    PUBLIC_LOGIN = auto()
    PUBLIC_ITEM_LIST = auto()
    PUBLIC_ITEM_DETAIL = auto()
    MEBER_CART = auto()
    MEMBER_ORDER_LIST = auto()
    MEMBER_ORDER_DETAIL = auto()

class UserRole(Enum):
    ADMIN = auto()
    MEMBER = auto()
