from pages.base_page import BasePage

class InventoryPage(BasePage):
    # 定位符
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
    ITEM_CARD = ".inventory_item"

    def get_products(self):
        """抓取当前页面所有商品数据"""
        print("抓取商品数据...")

        # 确保商品页面元素加载完成
        self.page.wait_for_selector(self.ITEM_CARD)

        # 获取所有商品卡片
        items = self.page.locator(self.ITEM_CARD).all()

        products_list = []
        for item in items:
            name = item.locator(self.ITEM_NAMES).inner_text()
            price = item.locator(self.ITEM_PRICES).inner_text()
            # 处理价格 “$29.99” -> 29.99
            price = float(price.replace("$", ""))

            products_list.append({
                "name": name,
                "price": price
            })

        print(f"共抓取到 {len(products_list)} 个商品")
        return products_list