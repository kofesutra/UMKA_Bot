import psycopg

from Config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_TABLE


def add_all_to_db(columns_here, data_here):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {DB_TABLE} ({columns_here}) VALUES ({data_here})")


def update_email_db(value, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET email = '{value}' WHERE id = {condition}")


def update_values_db(values, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET {values} WHERE id = {condition}")


def get_max_id(condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT MAX(id) FROM {DB_TABLE} WHERE user_id = {condition}")
        for z in cursor.fetchall():
            x = z[0]
        return x


def request_to_db_single(request, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE id = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x


def request_to_db_single_two(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x

# Ищем есть ли запись request в строках condition_name соответствующих условию condition


def request_to_db_column(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        return cursor.fetchall()


def request_to_db_column_two(request, condition_name, condition, condition_name_2, condition_2):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = '{condition}' AND {condition_name_2} = '{condition_2}'")
        # return cursor.fetchall()
        for z in cursor.fetchall():
            x = z[0]
            return x


def delete_from_db(line_with_condition, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {DB_TABLE} WHERE {line_with_condition} = '{condition}'")


def db_export():
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT * FROM {DB_TABLE}")
        cursor.execute(f"SELECT * FROM {DB_TABLE} ORDER BY date_of_use DESC")
        z = cursor.fetchall()
        return z


def db_export_short():
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, user_id, username, first_name, last_name, age, sex, date_of_use, email, state_of_use, come_from FROM {DB_TABLE}")
        z = cursor.fetchall()
        return z
