import sqlite3
from random import randint as rd


class Database:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

        # main table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INT PRIMARY KEY,
           username TEXT NULL,
           name_ TEXT NULL,
           gender TEXT NULL,
           city TEXT NULL,
           age TEXT NULL,
           description TEXT NULL,
           mbti TEXT NULL,
           tags TEXT NULL,
           photo BLOB NULL,
           filter_age INT NULL,
           filter_gender TEXT NULL,
           filter_city TEXT NULL);
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

    def replace_gender(self, id_user, gender_):
        sql = """UPDATE users SET gender = ? WHERE user_id = ?"""

        self.cur.execute(sql, (gender_, id_user))
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

    def replace_mbti(self, id_user, mbti_):
        sql = """UPDATE users SET mbti = ? WHERE user_id = ?"""

        self.cur.execute(sql, (mbti_, id_user))
        self.conn.commit()

    def get_mbti(self, id_user):
        sql = """SELECT mbti FROM users WHERE user_id = ?"""

        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

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

    def get_gender(self, id_user):
        sql = """ SELECT gender from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]
    def get_random_profile(self, id_user):
        sql = """ SELECT * from users where user_id != ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_my_profile(self, id_user):
        sql = """ SELECT * from users where user_id == ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchone()
        return info

    def get_tags(self, id_user):
        sql = """SELECT tags FROM users WHERE user_id == ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchone()
        return info[0]

    def replace_tags(self, id_user, tags_):
        sql = """UPDATE users SET tags = ? WHERE user_id = ?"""

        self.cur.execute(sql, (tags_, id_user))
        self.conn.commit()

    def get_photo(self, id_user):
        sql = """ SELECT photo from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def replace_photo(self, id_user, blob_photo):
        sql = """UPDATE users SET photo = ? WHERE user_id = ?"""

        self.cur.execute(sql, (blob_photo, id_user))
        self.conn.commit()

    def replace_filter_age(self, id_user, age):
        sql = """UPDATE users SET filter_age = ? WHERE user_id = ?"""

        self.cur.execute(sql, (age, id_user))
        self.conn.commit()

    def replace_filter_gender(self, id_user, gender):
        sql = """UPDATE users SET filter_gender = ? WHERE user_id = ?"""

        self.cur.execute(sql, (gender, id_user))
        self.conn.commit()

    def replace_filter_city(self, id_user, city):
        sql = """UPDATE users SET filter_city = ? WHERE user_id = ?"""

        self.cur.execute(sql, (city, id_user))
        self.conn.commit()

    def get_filter_gender(self, id_user):
        sql = """ SELECT filter_gender from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_filter_city(self, id_user):
        sql = """ SELECT filter_city from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]
    def get_filter_age(self, id_user):
        sql = """ SELECT filter_age from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_random_profile_gca(self, id_user, gender_, city_, age_):
        sql = """ SELECT * from users where user_id != ? and gender == ? and city == ? and age == ?"""

        self.cur.execute(sql, (id_user, gender_, city_, age_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_gc(self, id_user, gender_, city_):
        sql = """ SELECT * from users where user_id != ? and gender == ? and city == ?"""

        self.cur.execute(sql, (id_user, gender_, city_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_ga(self, id_user, gender_, age_):
        sql = """ SELECT * from users where user_id != ? and gender == ? and age == ?"""

        self.cur.execute(sql, (id_user, gender_, age_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_ca(self, id_user, city_, age_):
        sql = """ SELECT * from users where user_id != ? and city == ? and age == ?"""

        self.cur.execute(sql, (id_user, city_, age_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_g(self, id_user, gender_):
        sql = """ SELECT * from users where user_id != ? and gender == ?"""

        self.cur.execute(sql, (id_user, gender_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_a(self, id_user, age_):
        sql = """ SELECT * from users where user_id != ? and age == ?"""

        self.cur.execute(sql, (id_user, age_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]

    def get_random_profile_c(self, id_user, city_):
        sql = """ SELECT * from users where user_id != ? and city == ?"""

        self.cur.execute(sql, (id_user, city_))
        info = self.cur.fetchall()
        return info[rd(0, len(info) - 1)]
