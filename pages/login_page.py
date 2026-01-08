from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    登录页面模型 (Page Object)
    职责：封装所有与登录页相关的定位符和操作。
    """
    url = "https://saucedemo.com/"

    # ===============================
    # 1. 元素定位符 (UI Map)
    # ===============================
    # CSS 选择器：网页改版时，只需修改这里，不用改业务代码
    INPUT_USER = "#user-name"
    INPUT_PASSWORD = "#password"
    BUTTON_LOGIN = "#login-button"

    def login(self, username, password):
        """
        业务动作：执行登录操作
        这是一个原子操作，将'输入用户名' + '输入密码' + '点击登录' 封装在一起。
        """
        # 1. 打开页面
        self.open(self.url)
        
        # 2. 填写表单
        # Playwright 的 .fill() 方法会自动等待元素可见并可编辑
        self.page.fill(self.INPUT_USER, username)
        self.page.fill(self.INPUT_PASSWORD, password)
        
        # 3. 提交
        self.page.click(self.BUTTON_LOGIN)