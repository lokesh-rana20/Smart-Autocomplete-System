
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MYSQLPASS",
        database="autocomplete_db"
    )


def get_all_words():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT word FROM words")
        words = [row[0] for row in cursor.fetchall()]
        return words
    finally:
        cursor.close()
        connection.close()


def add_word_to_db(word):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO words (word) VALUES (%s)",
            (word,)
        )
        connection.commit()
        return True

    except mysql.connector.IntegrityError:
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

        
def increment_search_count(word):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE words
            SET search_count = search_count + 1
            WHERE word = %s
            """,
            (word,)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

        
def get_popular_words():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT word, search_count FROM words"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


