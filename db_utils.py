import sqlite3

print('hello')


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


conn = create_connection("C:\\Github\\amazon_scraper\\something.db")


def create_table():
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_info(
                            title TEXT PRIMARY KEY
                            , price TEXT
                            , ratings TEXT
                            , is_sponsored BOOL
                            );
        ''')
        conn.commit()
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while Creating tables...")


def insert_update(data):
    cursor = conn.cursor()
    try:
        sql = """
               INSERT OR REPLACE INTO product_info (title, price, ratings, is_sponsored)
               VALUES (?, ?, ?, ?)"""
        cursor.execute(
            sql,
            (
                data[0],
                data[1],
                data[2],
                data[3],
            ),
        )
        conn.commit()
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while inserting...")
