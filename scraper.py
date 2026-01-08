from playwright.sync_api import sync_playwright  # 导入 Playwright 同步 API，用于控制浏览器
from pages.login_page import LoginPage           # 导入登录页面的 Page Object 模型
from pages.inventory_page import InventoryPage   # 导入商品库存页面的 Page Object 模型
from database.db_manager import DBManager        # 导入数据库管理类，用于后续存储数据
from utils.logger import logger                  # 导入我们封装的日志工具 🚀

def run_scraper():
    """
    爬虫主入口函数。
    负责编排整个抓取流程：启动浏览器 -> 登录 -> 抓取 -> 存库。
    """
    scraped_products = []  # 初始化一个空列表，用来存放抓取到的商品数据

    # 使用 context manager (with 语句) 启动 Playwright
    # 这样可以确保代码执行完毕后，自动释放 Playwright 相关的资源，防止内存泄漏
    with sync_playwright() as p:
        # 1. 启动浏览器
        # headless=True 表示无头模式（不显示浏览器界面），适合生产环境或自动化运行
        # 如果需要调试看效果，可以改为 headless=False
        logger.info("正在启动浏览器 (Chrome Headless)...")
        browser = p.chromium.launch(headless=True)
        
        # 2. 创建浏览器上下文 (Context)
        # Context 相当于一个独立的浏览器会话（类似隐身窗口），不同 Context 之间 Cookie 不共享
        context = browser.new_context()
        
        # 3. 在上下文中打开一个新页面 (Page)
        # Page 相当于浏览器中的一个标签页
        page = context.new_page()

        # 4. 实例化 POM (Page Object Model) 对象
        # 将 page 传递给页面对象，让它们能操作这个页面
        login_page = LoginPage(page)          # 登录页操作对象
        inventory_page = InventoryPage(page)  # 商品列表页操作对象

        # 5. 执行业务流程
        try:
            # 5.1 执行登录
            logger.info("正在尝试登录 SauceDemo...")
            login_page.login("standard_user", "secret_sauce")
            logger.info("登录成功！")
            
            # 5.2 登录成功后，抓取商品数据
            logger.info("开始抓取商品列表...")
            scraped_products = inventory_page.get_products()
            logger.info(f"抓取完成，共获取 {len(scraped_products)} 条商品信息。")
            
        except Exception as e:
            # 捕获所有异常，防止因为页面加载失败等原因导致程序直接崩溃
            # 在面试中可以强调这点：保证程序的健壮性
            logger.error(f"抓取过程中发生错误: {e}")
            
        finally:
            # 6. 关闭浏览器
            # 放在 finally 块中，确保无论是否出错，浏览器都能被正确关闭
            logger.info("正在关闭浏览器...")
            browser.close()

    # 7. 数据持久化 (存入数据库)
    if scraped_products:
        logger.info("准备将数据存入数据库...")
        db = DBManager()                 # 实例化数据库管理器
        db.save_product(scraped_products) # 调用保存方法
        db.close()                       # 关闭数据库连接
        logger.success("所有流程执行完毕，数据已入库！")
    else:
        logger.warning("未抓取到任何商品数据，跳过数据库保存步骤。")
    
    return scraped_products

if __name__ == "__main__":
    # 当直接运行此文件时执行
    run_scraper()