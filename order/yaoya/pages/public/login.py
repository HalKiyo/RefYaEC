import streamlit as st
from yaoya.const import PageId
from yaoya.pages.base import BasePage
from yaoya.services.auth import AuthenticationError, IAuthAPIClientService
from yaoya.services.user import IUserAPIClientService


class LoginPage(BasePage):
    def render(self) -> None:
        # ページ描写
        st.title(self.title)
        with st.form("form"):
            user_id = st.text_input("UserID")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="ログイン",
                                                  on_click=self.auth_change_page,
                                                  args=(user_id, password))

    def auth_change_page(self, user_id: str, password: str) -> None:
        auth_api_client: IAuthAPIClientService = self.ssm.get_auth_api_client()
        user_api_client: IUserAPIClientService = self.ssm.get_user_api_client()

        try:
            session_id = auth_api_client.login(user_id, password)
            user = user_api_client.get_by_session_id(session_id)
        except AuthenticationError:
            st.sidebar.error("ユーザIDまたはパスワードが間違っています。")
            return

        # ログインに成功した場合、成功メッセージを表示する
        st.sidebar.success("ログインに成功しました。")
        self.ssm.set_user(user)
        self.ssm.set_session_id(session_id)

        # 商品一覧ページに遷移
        self.ssm.set_page_id(PageId.PUBLIC_ITEM_LIST)
