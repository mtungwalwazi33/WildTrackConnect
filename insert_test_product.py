import sqlite3
from pathlib import Path

db = Path(__file__).parent.joinpath('WildTrackConnect','db.sqlite3')
conn = sqlite3.connect(db)
c = conn.cursor()
# Insert a test product
c.execute("INSERT INTO store_product (name, description, price, stock, image) VALUES (?,?,?,?,?)", ('Automated Test Product', '', '9.99', 10, None))
conn.commit()
print('Inserted, lastid=', c.lastrowid)
conn.close()
