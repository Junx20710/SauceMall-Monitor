import pytest
import requests
import allure

API_URL = "http://127.0.0.1:5000/api/products"

@allure.feature("API 高级测试")
@allure.story("商品筛选接口测试")
class TestProductFilter:

    # ==========================
    # 理论应用 1: 有效等价类 (Valid Cases)
    # ==========================
    @allure.title("测试正常价格区间筛选")
    @pytest.mark.parametrize("min_p, max_p, expected_count", [
        (0, 100, 6),   # 全范围 (假设共6个商品)
        (0, 10, 1),    # 低价区 (根据 SauceDemo 数据，只有 Bike Light $9.99)
        (29.99, 29.99, 1), # 精确匹配 (边界值)
        (1000, 2000, 0) # 有效区间，但无数据
    ])
    def test_filter_valid_range(self, min_p, max_p, expected_count):
        params = {"min_price": min_p, "max_price": max_p}
        
        with allure.step(f"请求 API，参数: {params}"):
            response = requests.get(API_URL, params=params)
        
        assert response.status_code == 200
        data = response.json()['data']
        
        # 验证数量（这一步依赖于数据库里有固定的数据，实际工作中通常配合 Fixture 造数）
        # 这里我们主要验证逻辑：返回的每一个商品价格是否都在区间内
        for item in data:
            price = float(item['price'])
            assert min_p <= price <= max_p, f"商品价格 {price} 超出筛选范围!"

    # ==========================
    # 理论应用 2: 无效等价类 (Invalid Cases)
    # ==========================
    @allure.title("测试非法参数输入 (400错误)")
    @pytest.mark.parametrize("invalid_param, value", [
        ("min_price", "abc"),   # 字母
        ("max_price", "12.5.5"), # 非法数字格式
    ])
    def test_filter_invalid_input(self, invalid_param, value):
        params = {invalid_param: value}
        
        with allure.step(f"发送非法参数: {params}"):
            response = requests.get(API_URL, params=params)
        
        # 预期后端做了参数校验，返回 400
        assert response.status_code == 400
        assert "error" in response.json()

    # ==========================
    # 理论应用 3: 业务逻辑边界
    # ==========================
    @allure.title("测试逻辑矛盾区间 (Min > Max)")
    def test_filter_logic_conflict(self):
        # 最小值 50，最大值 10
        params = {"min_price": 50, "max_price": 10}
        response = requests.get(API_URL, params=params)
        
        assert response.status_code == 200
        # 应该返回空列表，而不是报错
        assert len(response.json()['data']) == 0