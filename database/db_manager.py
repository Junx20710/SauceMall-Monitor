import pymysql
import time
import sys

class DBManager:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3307
        self.user = 'saucemall_user'
        self.password = 'saucemall_password'
        self.db_name = 'saucemall'
        self.conn = None

    def connect(self):
        print("Connecting to the database...")
        for i in range(5):
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db_name,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Database connection established.")
                return
            except pymysql.MySQLError as e:
                print(f"Connection attempt {i+1} failed: {e}")
                time.sleep(2)
        print("Failed to connect to the database after 5 attempts.")
        sys.exit(1)
    
    def save_product(self, product_list):
        """批量保存商品数据到数据库"""
        if not self.conn:
            self.connect()
        
        # 插入商品数据的 SQL 语句
        sql = "INSERT INTO products (name, price) VALUES (%s, %s)"

        # 准备数据格式 [(name1, price1), (name2, price2), ...]
        data_to_insert = [(p['name'], p['price']) for p in product_list]

        try:
            with self.conn.cursor() as cursor:
                # 先清空旧数据
                cursor.execute("TRUNCATE TABLE products")
                # 批量插入新数据
                cursor.executemany(sql, data_to_insert)
            self.conn.commit()
            print(f"Inserted {len(product_list)} products into the database.")    
        except Exception as e:
            print(f"Failed to save products: {e}")
            self.conn.rollback()

            
    def init_table(self):
        """初始化商品表"""
        if not self.conn:
            self.connect()
        # 创建商品表： ID, name, price, created_at
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
            print("Table 'products' initialized successfully.")
        except pymysql.MySQLError as e:
            print(f"Failed to initialize table: {e}")
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    db_manager = DBManager()
    db_manager.connect()
    db_manager.init_table()
    db_manager.close()