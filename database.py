from random import randint, choice

class Database:
    @staticmethod
    def find_user_by_id(id, filename):
        file = open(filename + ".txt", "r", encoding="UTF-8")
        file.seek(0)
        for line in file.readlines():
            user_id = line.split()[0]
            if user_id == id:
                return True
        return False

    @staticmethod
    def write(users, filename):
        file = open(filename + ".txt", "w", encoding="UTF-8")
        for user, info in users.items():
            file.write(f"{user} {info['state']} {info['username']} {info['name']} {info['city']} {info['age']}"
                       f" {' '.join(info['likes'])}\n")

    @staticmethod
    def get_dict(filename):
        file = open(filename + ".txt", "r", encoding="UTF-8")
        file.seek(0)
        users = {}
        for line in file.readlines():
            line_list = line.split()
            id = line_list[0]
            state = line_list[1]
            username = line_list[2]
            name = line_list[3]
            city = line_list[4]
            age = line_list[5]
            likes = line_list[6:]
            users[id] = {"state": state, "username": username, "name": name, "city": city, "age": age, "likes": likes}
        return users

    @staticmethod
    def random_profile_list(filename, id):
        users = Database.get_dict(filename)
        # rand_i = randint(0, len(users) - 2)
        # i = 0
        users.pop(id)
        user_id = choice(list(users.keys()))
        info = users[user_id]
        user_info = [user_id, info["name"], info["city"], info["age"]]
        return user_info

    @staticmethod
    def get_my_profile(filename, id):
        file = open(filename + ".txt", "r", encoding="UTF-8")
        file.seek(0)
        for line in file.readlines():
            l = line.split()
            if l[0] == id:
                return [l[2], l[3], l[4]]

    # def get_profile_by_id



