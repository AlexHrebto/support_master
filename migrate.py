import sqlite3

count_db = "1"
k = 1

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

check_sql = cursor.execute("PRAGMA table_info(users)")
check_sql = check_sql.fetchall()
check_create_users = [c for c in check_sql]
if len(check_create_users) > 0:
    print(f"Table was found({k}/{count_db})")
else:
    cursor.execute("CREATE TABLE users("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "user_id INTEGER, username TEXT, "
                   "date_reg DATETIME, ref_code INTEGER)")
    print(f"Table was not found({k}/{count_db}) | Creating...")
k += 1


conn.commit()
conn.close()
