from pathlib import Path
from tempfile import TemporaryDirectory

from yaoya.app import MultiPageApp
from yaoya.const import PageId
from yaoya.pages.base import BasePage
from yaoya.pages.public.item_list import ItemListPage
from yaoya.pages.public.item_detail import ItemDetailPage
from yaoya.pages.public.login import LoginPage
from yaoya.services.auth import MockAuthAPIClientService
from yaoya.services.item import MockItemAPIClientService
from yaoya.services.mock import MockDB, MockSessionDB
from yaoya.services.user import MockUserAPIClientService
from yaoya.session import StreamlitSessionManager

# session_stateの初期化
def init_session() -> StreamlitSessionManager:
    mockdir = Path(TemporaryDirectory().name)
    mockdir.mkdir(exist_ok=True)
    mockdb = MockDB(mockdir.joinpath("mock.db"))
    session_db = MockSessionDB(mockdir.joinpath("session.json"))
    ssm = StreamlitSessionManager(
        auth_api_client=MockAuthAPIClientService(mockdb, session_db),
        user_api_client=MockUserAPIClientService(mockdb, session_db),
        item_api_client=MockItemAPIClientService(mockdb)
    )
    return ssm

# ページの初期化
def init_pages(ssm: StreamlitSessionManager) -> list[BasePage]:
    pages = [
        LoginPage(page_id=PageId.PUBLIC_LOGIN.name, title="ログイン", ssm=ssm),
        ItemListPage(page_id=PageId.PUBLIC_ITEM_LIST, title="商品一覧", ssm=ssm),
        ItemDetailPage(page_id=PageId.PUBLIC_ITEM_DETAIL, title="商品詳細", ssm=ssm)
    ]
    return pages

# アプリケーションの初期化
def init_app(ssm: StreamlitSessionManager, pages: list[BasePage]) -> MultiPageApp:
    app = MultiPageApp(ssm, pages)
    return app
