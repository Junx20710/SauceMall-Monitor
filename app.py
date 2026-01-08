from flask import Flask, jsonify, request
from database.db_manager import DBManager
from utils.logger import logger  # 导入日志

app = Flask(__name__)

# ===============================
# API 定义部分
# ===============================

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    获取商品列表接口
    支持筛选参数: min_price, max_price
    """
    # 记录请求日志
    logger.info(f"收到 API 请求: {request.full_path}")
    
    db = DBManager()
    
    # 1. 获取 URL 参数
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    try:
        db.connect()
        with db.conn.cursor() as cursor:
            # ===============================
            # 2. 动态 SQL 构建 (Dynamic SQL)
            # ===============================
            sql = "SELECT name, price, scraped_at FROM products WHERE 1=1"
            params = []

            # 2.1 处理 min_price 参数
            if min_price:
                try:
                    sql += " AND price >= %s"
                    params.append(float(min_price))
                except ValueError:
                    logger.warning(f"Invalid min_price parameter: {min_price}")
                    return jsonify({"code": 400, "error": "min_price must be a number"}), 400
            
            # 2.2 处理 max_price 参数
            if max_price:
                try:
                    sql += " AND price <= %s"
                    params.append(float(max_price))
                except ValueError:
                    logger.warning(f"Invalid max_price parameter: {max_price}")
                    return jsonify({"code": 400, "error": "max_price must be a number"}), 400

            # ===============================
            # 3. 执行查询
            # ===============================
            logger.debug(f"执行 SQL: {sql} | Params: {params}")
            cursor.execute(sql, params)
            results = cursor.fetchall()
        
        logger.info(f"查询成功，返回 {len(results)} 条数据")
        
        # 4. 返回标准 JSON 格式
        return jsonify({
            "code": 200,
            "message": "success",
            "data": results,
            "total": len(results)
        })

    except Exception as e:
        # 5. 全局异常兜底
        logger.error(f"API Internal Error: {e}")
        return jsonify({"code": 500, "error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口 (Health Check) - 供运维监控使用"""
    # 健康检查一般跑得很频繁，用 debug 级别避免刷屏，或者 info 级别看心跳
    # 这里用 debug
    logger.debug("Health Check Request received.")
    return jsonify({
        "status": "ok",
        "message": "API is running"
    })

if __name__ == '__main__':
    # host='0.0.0.0' 允许外网访问（Docker 容器内必须这么设）
    logger.info("Flask Server Starting on port 5000...")
    app.run(host='0.0.0.0', port=5000)