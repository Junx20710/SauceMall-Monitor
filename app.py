from flask import Flask, jsonify , request
from database.db_manager import DBManager

app = Flask(__name__)
@app.route('/api/products', methods=['GET'])
def get_products():
    db = DBManager()
    
    # 1. 获取 URL 参数
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    try:
        db.connect()
        with db.conn.cursor() as cursor:
            # 基础 SQL
            sql = "SELECT name, price, scraped_at FROM products WHERE 1=1"
            params = []

            # 2. 动态拼接 SQL (模拟业务逻辑)
            if min_price:
                # 【测试点】如果传入非数字，这里 float() 会报错，我们要捕获它
                try:
                    sql += " AND price >= %s"
                    params.append(float(min_price))
                except ValueError:
                    return jsonify({"code": 400, "error": "min_price must be a number"}), 400
            
            if max_price:
                try:
                    sql += " AND price <= %s"
                    params.append(float(max_price))
                except ValueError:
                    return jsonify({"code": 400, "error": "max_price must be a number"}), 400

            cursor.execute(sql, params)
            results = cursor.fetchall()
        
        return jsonify({
            "code": 200,
            "message": "success",
            "data": results,
            "total": len(results)
        })
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "API is running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)