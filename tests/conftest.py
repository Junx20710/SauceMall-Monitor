import pytest
from database.db_manager import DBManager

@pytest.fixture(scope="function")
def clean_db():
    """
    fixture 测试前置操作
    在每个测试函数前初始化数据库表，并在测试后清空数据库表
    """
    db = DBManager()
    db.connect()
    try:
        with db.conn.cursor() as cursor:
            # TRUNCATE 比 DELETE 更快且重置自增ID
            cursor.execute("TRUNCATE TABLE products")
        db.conn.commit()
        print("✨ [Fixture] 数据库清理完毕。")
    except Exception as e:
        print(f"⚠️ [Fixture] 清理数据库时出错: {e}")
    finally:
        db.close()
    yield
    # 测试后清理数据库 