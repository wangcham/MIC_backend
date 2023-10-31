import mysql.connector

database_config = {
  'user': 'root',
  'password': 'superbl',
  'host': 'localhost',  
  'database': 'dachuang',
  'port': '3306',
  'charset': 'utf8mb4'
}

class Database:                          
  def __init__(self, app=None):
    self.app = app
    self.db_config = None

  def get_conn(self):
    self.db_config = database_config
    return mysql.connector.connect(**self.db_config)

  def execute(self, query, args=None):
    conn = None
    cursor = None
    try:
        conn = self.get_conn()
        cursor = conn.cursor()
        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()

        return results
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
        return str(e)
    finally:
        if cursor:
            cursor.close()  # 关闭游标
        if conn:
            conn.close()
  #创建表
  def create_tables(self,query):
    self.execute(query)

  #删除表 
  def drop_all_tables(self):
      drop_tables_query = "SHOW TABLES"
      try:
          conn = self.get_conn()
          cursor = conn.cursor()
          cursor.execute(drop_tables_query)
          tables = cursor.fetchall()
          for table in tables:
              table_name = table[0]
              drop_table_query = f"DROP TABLE {table_name}"
              cursor.execute(drop_table_query)
          conn.commit()
          return "所有表已删除"
      except Exception as e:
          if conn:
              conn.rollback()
          return str(e)
      finally:
          if cursor:
              cursor.close()
          if conn:
              conn.close()

#建表语句

create_tables_query = """
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT UNIQUE PRIMARY KEY,
    username VARCHAR(50),
    sex VARCHAR(50),
    age INT,
    doctor_id INT,
    status TEXT,
    imagepath VARCHAR(255),
    segpath VARCHAR(255),
    telephone VARCHAR(50),
    surgery TINYINT(1),
    password VARCHAR(50),
    avatarurl VARCHAR(255),
    name VARCHAR(50),
);

CREATE TABLE IF NOT EXISTS doctors (
id INT AUTO_INCREMENT  UNIQUE PRIMARY KEY,
name VARCHAR(50),
username VARCHAR(50),
telephone VARCHAR(50),
password VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS gpt_histories(
patient_id INT,
chat TEXT,
time DATETIME
);

CREATE TABLE IF NOT EXISTS uploaded_images(
doctor_id INT,
image_path VARCHAR(255)

);
"""




