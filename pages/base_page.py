from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self,url):
        # 通用方法，打开指定页面
        self.page.goto(url)

        # 等待页面加载完成 (networkidle代表网络空闲)
        self.page.wait_for_load_state("networkidle")

    def get_text(self, selector):
        # 通用方法，获取指定选择器的文本内容
        return self.page.text_content(selector)