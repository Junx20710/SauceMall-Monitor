import pymysql
import os
import time
import sys
from utils.logger import logger  # 导入日志模块

class DBManager:
    """
    数据库管理类
    负责处理所有与 MySQL 数据库的交互，包括连接、初始化表、保存数据。
    """
    def __init__(self):
        # 从环境变量获取配置，如果不存在这使用默认值（方便本地调试）
        # 在 Docker 环境中，这些变量会在 docker-compose.yml 中注入
        self.host = os.getenv('DB_HOST', '127.0.0.1')
        self.port = int(os.getenv('DB_PORT', 3307)) # 本地映射端口 3307
        self.user = os.getenv('DB_USER', 'saucemall_user')
        self.password = os.getenv('DB_PASSWORD', 'saucemall_password')
        self.db_name = os.getenv('DB_NAME', 'saucemall')
        self.conn = None

    def connect(self):
        """
        建立数据库连接 (带重试机制)
        面试亮点：为什么需要重试？
        因为数据库容器启动往往比爬虫慢，或者网络会出现短暂抖动。
        """
        logger.info(f"正在连接数据库 {self.host}:{self.port}...")
        # 尝试连接 5 次
        for i in range(5):
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db_name,
                    charset='utf8mb4',
                    # 返回字典类型的游标，方便通过列名访问数据 (e.g., row['price'])
                    cursorclass=pymysql.cursors.DictCursor
                )
                logger.info("数据库连接成功 established.")
                # 连接成功后顺便初始化表
                self.init_table()
                return
            except pymysql.MySQLError as e:
                # 连接失败，打印错误并等待 2 秒后重试
                logger.warning(f"Connection attempt {i+1} failed: {e}. Retrying in 2s...")
                time.sleep(2)
        
        # 5次都失败，程序退出
        logger.critical("Failed to connect to the database after 5 attempts.")
        sys.exit(1)
    
    def save_product(self, product_list):
        """
        批量保存商品数据
        面试亮点：事务 (Transaction) + 批量插入 (Batch Insert)
        """
        if not self.conn:
            self.connect()
        
        try:
            # 使用 Context Manager 自动关闭游标
            with self.conn.cursor() as cursor:
                # 1. 事务开始：先清空旧数据 (TRUNCATE)
                # TRUNCATE 比 DELETE 速度快，且会重置自增 ID
                logger.info("正在清空旧数据 (TRUNCATE)...")
                cursor.execute("TRUNCATE TABLE products")
                
                # 2. 准备 SQL 语句
                # 使用 %s 占位符防止 SQL 注入
                sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
                
                # 3. 准备数据格式
                # 将字典列表转换为 tuple 列表: [('Bag', 29.99), ('Light', 9.99)]
                data_to_insert = [
                    (p['name'], float(p['price'])) 
                    for p in product_list
                ]
                
                # 4. 批量执行插入 (Batch Insert)
                # 相比于在 for 循环里一条条 insert，executemany 性能高出 10 倍以上
                logger.info(f"正在批量插入 {len(data_to_insert)} 条数据...")
                cursor.executemany(sql, data_to_insert)
            
            # 5. 提交事务 (Commit)
            # 只有 commit 了，数据才会真正写入硬盘
            self.conn.commit()
            logger.success("数据保存成功！(Committed)")
            
        except pymysql.MySQLError as e:
            # 6. 回滚事务 (Rollback)
            # 如果中间任何一步出错，撤销所有操作，保证数据库不脏
            self.conn.rollback()
            logger.error(f"Error saving data: {e}. Transaction Rolled Back.")

    def init_table(self):
        """
        初始化数据表结构
        """
        if not self.conn:
            return # Should be called inside connect usually, or check conn
            
        sql = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) 
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            logger.debug("Table 'products' initialized/verified.")
        except pymysql.MySQLError as e:
            logger.error(f"Failed to initialize table: {e}")
    
    def close(self):
        """关闭数据库连接，释放资源"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    # 本地测试代码
    db = DBManager()
    db.connect()
    db.close()