from pages.base_page import BasePage

class LoginPage(BasePage):
    url = "https://saucedemo.com/"

    # 定位符 网页改变只修改这里
    INPUT_USER = "#user-name"
    INPUT_PASSWORD = "#password"
    BUTTON_LOGIN = "#login-button"

    def login(self , username , password):
        """执行登录操作"""
        self.open(self.url)
        self.page.fill(self.INPUT_USER, username)
        self.page.fill(self.INPUT_PASSWORD, password)
        self.page.click(self.BUTTON_LOGIN)