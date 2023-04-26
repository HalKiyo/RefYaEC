from typing import Protocol

import dataset
from yaoya.exceptions import YaoyaError
from yaoya.models.session import Session
from yaoya.services.mock import MockDB, MockSessionDB

class AuthenticationError(YaoyaError):
    pass

class IAuthAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> str:
        pass

class MockAuthAPIClientService(IAuthAPIClientService):
    def __init__(self, mockdb: MockDB, session_db: MockSessionDB) -> None:
        self.mockdb = mockdb
        self.session_db = session_db

    # ログインに成功した場合、MockSessionDBにセッションを追加し、セッションIDを返す
    # ログインに失敗した場合、AuthenticationErrorを発生させる
    def login(self, user_id: str, password: str) -> str:
        if not self._verify_user(user_id, password):
            raise AuthenticationError

        session = Session(user_id=user_id)
        with self.session_db.connect() as db:
            db.insert(session.to_dict())

        return session.session_id

    # 指定されたユーザIDを持つユーザがMockDBのユーザテーブルに入ればTrueを返す
    # *パスワードの検証は行わない
    def _verify_user(self, user_id: str, password: str) -> bool:
        with self.mockdb.connect() as db:
            table: dataset.Table = db["users"]
            user_data = table.find_one(user_id=user_id)

        return user_data is not None
