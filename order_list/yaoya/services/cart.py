from collections.abc import Callable
from typing import Protocol

from tinydb import Query
from yaoya.models.cart import Cart, CartItem
from yaoya.models.session import Session
from yaoya.services.mock import MockSessionDB


class ICartAPIClientService(Protocol):
    def get_cart(self, session_id: str) -> Cart:
        pass

    def add_item(self, session_id: str, cart_item: CartItem) -> None:
        pass

    def clear_cart(self, session_id: str) -> None:
        pass


class MockCartAPIClientService(ICartAPIClientService):
    def __init__(self, session_db: MockSessionDB) -> None:
        self.session_db = session_db

    def get_cart(self, session_id: str) -> Cart:
        with self.session_db.connect() as db:
            query = Query()
            session_dict = db.search(query.session_id == session_id)[0]
            session = Session.from_dict(session_dict)

        return session.cart

    def add_item(self, session_id: str, cart_item: CartItem) -> None:
        with self.session_db.connect() as db:
            query = Query()
            # セッションテーブルの更新。TinyDBはコールバック関数を渡して更新可能
            db.update(self._get_add_item_cb(cart_item), query.session_id == session_id)


    def _get_add_item_cb(self, cart_item: CartItem) -> Callable[[dict], None]:
        def transform(doc: dict) -> None:

            session = Session.from_dict(doc)
            cart = session.cart
            new_cart_items = [*cart.cart_items, cart_item]

            # カート内の合計金額を更新
            new_total_price = cart_item.item.price * cart_item.quantity + cart.total_price
            # データクラスはイミュータブルなので、データクラスを新たに作成し、既存のレコードを置き換える
            new_cart = Cart(
                cart.user_id,
                cart_items=new_cart_items,
                total_price=new_total_price
            )
            new_session = Session(
                user_id=session.user_id,
                session_id=session.session_id,
                cart=new_cart
            )

            for key, value in new_session.to_dict().items():
                doc[key] = value


        return transform

    def clear_cart(self, session_id: str) -> None:
        with self.session_db.connect() as db:
            query = Query()
            db.update(self._get_clear_cart_cb(), query.session_id ==session_id)

    def _get_clear_cart_cb(self) -> Callable[[dict], None]:
        def transform(doc: dict) -> None:
            session = Session.from_dict(doc)
            new_session = Session(
                session_id=session.session_id,
                user_id=session.user_id,
                cart=Cart(user_id=session.user_id)
            )
            for key, value in new_session.to_dict().items():
                doc[key] = value

        return transform
