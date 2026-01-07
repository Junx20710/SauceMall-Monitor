import pytest
import requests
import allure  
from scraper import run_scraper

@allure.feature("SauceMall 全链路测试")
class TestSauceMallE2E:
    
    @allure.story("数据一致性校验 (E2E)")
    @allure.title("验证 UI 抓取数据与 API 返回数据的一致性")
    @allure.description("流程：爬虫抓取 -> 数据库存储 -> API 查询 -> 数据比对")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_crawl_and_api_consistency(self, clean_db):
        
        with allure.step("Step 1: 启动爬虫抓取数据 (UI -> DB)"):
            print("\n🚀 Step 1: 启动爬虫...")
            scraped_data = run_scraper()
            allure.attach(str(scraped_data), name="爬虫抓取到的数据", attachment_type=allure.attachment_type.TEXT)
            assert scraped_data, "❌ 爬虫未抓取到任何数据！"

        with allure.step("Step 2: 调用后端 API 查询数据 (DB -> API)"):
            print("🚀 Step 2: 调用 API 查询...")
            api_url = "http://127.0.0.1:5000/api/products"
            try:
                response = requests.get(api_url)
            except requests.exceptions.ConnectionError:
                pytest.fail("❌ 无法连接 API")
            
            assert response.status_code == 200
            api_json = response.json()
            api_data = api_json['data']
            allure.attach(str(api_data), name="API 返回的数据", attachment_type=allure.attachment_type.JSON)

        with allure.step("Step 3: 执行数据比对 (Data Verification)"):
            print("🚀 Step 3: 执行数据比对...")
            # ... (下面的断言逻辑保持不变) ...
            assert len(scraped_data) == len(api_data)
            
            api_dict = {item['name']: float(item['price']) for item in api_data}
            for item in scraped_data:
                name = item['name']
                price = float(item['price'])
                with allure.step(f"校验商品: {name}"):
                    assert name in api_dict
                    assert price == api_dict[name]

        print("🎉🎉🎉 全链路测试通过！")