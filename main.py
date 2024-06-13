import sqlite3
with sqlite3.connect('register.db') as con:
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER CHECK(age > 0 AND age < 150),
            phone_number BLOB NOT NULL DEFAULT "+79090000000",
            email TEXT UNIQUE,
            address TEXT)
    """)


def add_user():
    added_users = []
    answer = 1
    while answer:
        first_name = input("first name:  ").title()
        last_name = input("last name: ").title()
        age = int(input("age: "))
        phone_number = input("phone number: ")
        email = input("email: ")
        address = input("address: ")

        user = cur.execute(f"""
            INSERT INTO users(first_name, last_name, age, phone_number, email, address)
            VALUES("{first_name}", "{last_name}", {age}, "{phone_number}", "{email}", "{address}")
            returning *
        """).fetchone()
        added_users.append(user)
        con.commit()
        answer = int(input("Добавить еще одного пользователя?  Да ( 1 ),  Нет ( 0 ) >>> "))

    return added_users


def update_user():
    updated_user = []
    answer = 1
    while answer:
        user_id = int(input('user_id to update: '))
        column_name = input('column name: ').lower()
        if column_name == 'age':
            new_value = int(input("new value: "))
        else:
            new_value = input('new value: ')

        user = cur.execute(f"""
            UPDATE users
            SET  {column_name} = "{new_value}"
            WHERE id = {user_id}
            returning *   
        """).fetchone()

        updated_user.append(user)
        con.commit()
        answer = int(input("Изминить еще одного пользователя?  Да ( 1 ),  Нет ( 0 ) >>> "))

    return updated_user


def delete_user():
    deleted_user = []
    answer = 1
    while answer:
        user_id = input("user id to delete: ")

        user = cur.execute(f"""
            DELETE FROM users
            WHERE id = {user_id}
            returning *
        """).fetchone()
        deleted_user.append(user)
        con.commit()

        answer = int(input("Удалить еще одного пользователя?  Да ( 1 ),  Нет ( 0 ) >>> "))

    return deleted_user


def view_table():
    table_name = input('Имя таблицы >>> ')
    table = cur.execute(f"""
        SELECT * FROM "{table_name}"
    """).fetchall()
    return print(table)


def register():
    x = 1
    while x:
        answer = int(input("Добавить ( 1 ) , Изминить ( 2 ), Удалить ( 3 ), Посмотреть таблицу ( 4 ), Прекратить ( 0 )>>> "))
        if answer == 1:
            add_user()

        elif answer == 2:
            update_user()
        elif answer == 3:
            delete_user()
        elif answer == 4:
            view_table()
        elif answer == 0:
            x = answer

    return "Спасибо, что попробовали приложение"


print(register())











