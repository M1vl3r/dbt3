import mysql.connector

# Функция для выполнения SQL-запроса
def execute_query(connection, query):
    cursor = connection.cursor(dictionary=True)
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
            database='city_duma',
            user='root',
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
        task_number = int(input("Введите номер задания (1-7): "))

        # Выполнение соответствующего SQL-запроса
        if task_number == 1:
            query = "SELECT CommissionName, Chairman FROM Commissions;"
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 2:
            # Добавление нового члена комиссии
            query = "INSERT INTO CommissionMembers (CommissionID, MemberName) VALUES (1, 'Новый член');"
            execute_query(connection, query)
            print("Новый член комиссии добавлен успешно.")
        elif task_number == 3:
            query = "SELECT MemberName, CommissionName FROM CommissionMembers JOIN Commissions USING (CommissionID);"
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 4:
            # Добавление новой комиссии
            query = "INSERT INTO Commissions (CommissionName, Chairman) VALUES ('Новая комиссия', 'Председатель');"
            execute_query(connection, query)
            print("Новая комиссия добавлена успешно.")
        elif task_number == 5:
            # За указанный интервал дат и комиссии выдать список членов с указанием количества пропущенных заседаний
            query = "SELECT MemberName, CommissionName, MissedMeetings FROM CommissionMembers WHERE MeetingDate BETWEEN '2022-01-01' AND '2022-12-31';"
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 6:
            # Добавление нового заседания
            query = "INSERT INTO Meetings (CommissionID, MeetingDate, Organizer) VALUES (1, '2022-12-31', 'Организатор');"
            execute_query(connection, query)
            print("Новое заседание добавлено успешно.")
        elif task_number == 7:
            # По каждой комиссии показать количество проведенных заседаний в указанный период времени
            query = "SELECT CommissionName, COUNT(*) AS MeetingsCount FROM Meetings JOIN Commissions USING (CommissionID) WHERE MeetingDate BETWEEN '2022-01-01' AND '2022-12-31' GROUP BY CommissionName;"
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        else:
            print("Некорректный номер задания. Введите число от 1 до 7.")
    finally:
        # Закрываем соединение с базой данных
        connection.close()

if __name__ == "__main__":
    main()
