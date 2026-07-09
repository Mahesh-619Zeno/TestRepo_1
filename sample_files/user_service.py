import sqlite3

DB_PATH = "users.db"

def get_user_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
    result = cur.fetchall()
    conn.close()
    return result

def delete_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()

def update_user_status(user_id, status):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET status = '{status}' WHERE id = {user_id}")
    conn.commit()
    conn.close()

def main():
    print(get_user_by_name("Alice"))
    delete_user_by_id(2)
    update_user_status(1, "active")

if __name__ == "__main__":
    main()
