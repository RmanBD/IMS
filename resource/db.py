import sqlite3 as sq3

class InventoryDatabase:
    def __init__(self, db_file):
        self.conn = sq3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id TEXT PRIMARY KEY,
                name TEXT,
                in_stock INTEGER)
                            ''')
        self.conn.commit()

    def fetch_products(self):
        self.cursor.execute('SELECT * FROM Products')
        products = self.cursor.fetchall()
        return products

    def insert_product(self, id, name, in_stock):
        if not id.startswith('#'):
            id = '#' + id
        self.cursor.execute('INSERT INTO Products (id, name, in_stock) VALUES (?, ?, ?)',
                            (id, name, in_stock))
        self.conn.commit()

    def delete_product(self, id):
        self.cursor.execute('DELETE FROM Products WHERE id = ?', (id,))
        self.conn.commit()

    def update_product(self, new_name, new_stock, id):
        self.cursor.execute('UPDATE Products SET name = ?, in_stock = ? WHERE id = ?',
                            (new_name, new_stock, id))
        self.conn.commit()

    def id_exists(self, id):
        self.cursor.execute('SELECT COUNT(*) FROM Products WHERE id = ?', (id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def close(self):
        self.conn.close()

