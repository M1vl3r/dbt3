import mysql.connector

# Функция для выполнения SQL-запроса
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Функция для подключения к базе данных
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='dbt6',
            user='root',
            password='ваш_пароль'  # Укажите свой пароль
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Основная функция
def main():
    # Подключаемся к базе данных
    connection = connect_to_database()

    if not connection:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        # Запрос номера задания
        task_number = int(input("Введите номер задания (1-4): "))

        # Выполнение соответствующего SQL-запроса
        if task_number == 1:
            query = "SELECT SUM(Copies) AS TotalCopies FROM Keeping WHERE ID_Vault = 1 AND ID_Book = 1;"
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 2:
            query = """
                SELECT COUNT(DISTINCT p.ID_Faculty) AS FacultiesCount,
                       GROUP_CONCAT(DISTINCT f.Name_F) AS FacultyNames
                FROM Process p
                JOIN Faculties f ON p.ID_Faculty = f.ID_Faculty
                WHERE p.ID_Book = 1 AND p.ID_Faculty IN (
                    SELECT p.ID_Faculty FROM Keeping k WHERE k.ID_Vault = 1
                );
            """
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 3:
            query = """
                INSERT INTO Books (ID_Book, Name, Author, Publishers, Year_P, Cost, Scientific)
                VALUES (6, 'Новая книга', 'Новый автор', 'Новое издательство', 2023, 29.99, 1)
                ON DUPLICATE KEY UPDATE
                Name = VALUES(Name), Author = VALUES(Author), Publishers = VALUES(Publishers),
                Year_P = VALUES(Year_P), Cost = VALUES(Cost), Scientific = VALUES(Scientific);
            """
            execute_query(connection, query)
            print("Запрос выполнен успешно.")
        elif task_number == 4:
            query = """
                INSERT INTO Vault (ID_Vault, FIO_Leader, Address, Phone, Capacity)
                VALUES (6, 'Новый руководитель', 'Новый адрес', '9876543210', 150)
                ON DUPLICATE KEY UPDATE
                FIO_Leader = VALUES(FIO_Leader), Address = VALUES(Address),
                Phone = VALUES(Phone), Capacity = VALUES(Capacity);
            """
            execute_query(connection, query)
            print("Запрос выполнен успешно.")
        else:
            print("Некорректный номер задания. Введите число от 1 до 4.")
    finally:
        # Закрываем соединение с базой данных
        connection.close()

if __name__ == "__main__":
    main()
