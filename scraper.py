from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from database.db_manager import DBManager
import pprint

def run_scraper():
    # 启动 Playwright
    scraped_products = []
    with sync_playwright() as p:
        # 启动浏览器 headless=False 显示浏览器界面
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

       # 实例化 POM对象
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        # 执行业务流程
        # 登录标准账号
        try:
            login_page.login("standard_user", "secret_sauce")
            scraped_products = inventory_page.get_products()
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            browser.close()

    # 存入数据库
    if scraped_products:
        print("Saving products to database...")
        db = DBManager()
        db.save_product(scraped_products)
        db.close()
    else:
        print("No products scraped, skipping database save.")
    
    return scraped_products

if __name__ == "__main__":
    run_scraper()