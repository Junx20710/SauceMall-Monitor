from playwright.sync_api import Page

class BasePage:
    """
    基础页面类 (Parent Class)
    职责：存放所有页面共用的方法和属性。
    所有具体的 Page Object (如 LoginPage) 都继承自这个类。
    """
    def __init__(self, page: Page):
        # 接收一个 playwright helper对象，供所有子类使用
        self.page = page

    def open(self, url):
        """
        通用方法：打开指定 URL 并等待网络空闲。
        这比单纯的 page.goto(url) 更稳健，因为它会等待页面上的网络请求（如 AJAX）稍微消停一会。
        """
        self.page.goto(url)
        # "networkidle": 至少 500ms 内没有新的网络连接
        self.page.wait_for_load_state("networkidle")

    def get_text(self, selector):
        """通用方法：获取元素的文本"""
        return self.page.text_content(selector)