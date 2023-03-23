import sqlite3


class Database:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

        # main table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INT PRIMARY KEY,
           username TEXT NULL,
           name_ TEXT NULL,
           city TEXT NULL,
           age TEXT NULL,
           description TEXT NULL,
           mbti TEXT NULL);
        """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_state(
                   user_id INT PRIMARY KEY,
                   state_ TEXT,
                   active TEXT);
                """)

        self.conn.commit()

    def add_user(self, id_user, username):
        sql = """
                INSERT INTO users (user_id, username)
                VALUES (?, ?)
                """

        self.cur.execute(sql, (id_user, username))
        self.conn.commit()

    def add_user_state(self, id_user, s, a):
        sql = """
            INSERT INTO users_state (user_id, state_, active)
            VALUES (?, ?, ?)
            """

        self.cur.execute(sql, (id_user, s, a))
        self.conn.commit()

    def replace_state(self, id_user, s):
        sql = """UPDATE users_state SET state_ = ? WHERE user_id = ?"""

        self.cur.execute(sql, (s, id_user))

    def replace_name(self, id_user, name):
        sql = """UPDATE users SET name_ = ? WHERE user_id = ?"""

        self.cur.execute(sql, (name, id_user))
        self.conn.commit()

    def replace_city(self, id_user, city):
        sql = """UPDATE users SET city = ? WHERE user_id = ?"""

        self.cur.execute(sql, (city, id_user))
        self.conn.commit()

    def replace_age(self, id_user, age):
        sql = """UPDATE users SET age = ? WHERE user_id = ?"""

        self.cur.execute(sql, (age, id_user))
        self.conn.commit()

    def replace_description(self, id_user, description):
        sql = """UPDATE users SET description = ? WHERE user_id = ?"""

        self.cur.execute(sql, (description, id_user))
        self.conn.commit()

    def replace_active(self, id_user, act):
        sql = """UPDATE users_state SET active = ? WHERE user_id = ?"""

        self.cur.execute(sql, (act, id_user))
        self.conn.commit()

    def count_row_users(self, id_users):
        sql = """ SELECT COUNT(*) FROM users"""
        self.cur.execute(sql)
        return self.cur.fetchone()[0]

    def get_state(self, id_user):
        sql = """ SELECT state_ from users_state where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_random_profile(self, id_user):
        sql = """ SELECT * from users where user_id != ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchall()
        return info

    def get_my_profile(self, id_user):
        sql = """ SELECT * from users where user_id == ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchone()
        return info
