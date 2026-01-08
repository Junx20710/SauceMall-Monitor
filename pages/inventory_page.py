from pages.base_page import BasePage

class InventoryPage(BasePage):
    # ===============================
    # 1. 页面元素定位符 (Locators)
    # ===============================
    # CSS 选择器：找到所有商品卡片的容器
    ITEM_CARD = ".inventory_item"
    # CSS 选择器：在卡片内部找到商品名称
    ITEM_NAMES = ".inventory_item_name"
    # CSS 选择器：在卡片内部找到商品价格
    ITEM_PRICES = ".inventory_item_price"

    def get_products(self):
        """
        核心抓取方法：
        1. 等待元素加载
        2. 找到所有商品
        3. 循环提取数据
        4. 数据清洗
        """
        print("抓取商品数据...")

        # ===============================
        # 2. 智能等待 (Auto-waiting)
        # ===============================
        # 这一步非常重要！网页是动态加载的，必须等元素出现在 DOM 中才能操作。
        # Playwright 会自动等待，但显式调用 wait_for_selector 更稳健。
        self.page.wait_for_selector(self.ITEM_CARD)

        # ===============================
        # 3. 获取元素列表
        # ===============================
        # query_selector_all 的现代替代品。
        # 这里拿到的是一个 Locator 对象的列表，代表了页面上所有的商品卡片。
        items = self.page.locator(self.ITEM_CARD).all()

        products_list = []
        # ===============================
        # 4. 遍历与数据提取
        # ===============================
        for item in items:
            # 在当前卡片(item)的范围内查找名称和价格
            # inner_text() 会获取元素内的可见文本
            name = item.locator(self.ITEM_NAMES).inner_text()
            price_text = item.locator(self.ITEM_PRICES).inner_text()
            
            # ===============================
            # 5. 数据清洗 (Data Cleaning)
            # ===============================
            # 原始价格可能是 "$29.99"，数据库存的是数字。
            # 需要去掉 "$" 符号并转为浮点数。
            price = float(price_text.replace("$", ""))

            # 组装成字典
            products_list.append({
                "name": name,
                "price": price
            })

        print(f"共抓取到 {len(products_list)} 个商品")
        return products_list