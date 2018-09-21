import psycopg2
import config


class User:
    """
    class for user where:
        id
        chat_id
        first_name
        city
        country
        city_id
    """

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=config.DATABASE['name'],
            user=config.DATABASE['user'],
            password=config.DATABASE['password']
        )
        self.cursor = self.connection.cursor()

    def get_all_users(self):
        """Get all users from DB"""
        with self.connection:
            self.cursor.execute(
                """
                SELECT * FROM users;
                """
            )
            return self.cursor.fetchall()

    # (1, 227836750, 'Рафаэль', 'Kazan', 'RU', 551487)
    def get_user_by_chat_id(self, chat_id):
        """Get one user, by his chat_id"""
        with self.connection:
            self.cursor.execute(
                """
                SELECT * FROM users WHERE chat_id = %(chat_id)s;
                """,
                {'chat_id': chat_id}
            )
            return self.cursor.fetchone()

    def is_user_exist(self, chat_id):
        """Check the exist user in DB"""
        user = self.get_user_by_chat_id(chat_id)
        if user is None:
            return False
        else:
            return True

    def set_user(self, chat_id, first_name):
        """Insert new user in DB"""
        with self.connection:
            self.cursor.execute(
                """
                INSERT INTO users (chat_id, first_name)
                VALUES (%(new_user_chat_id)s, %(new_user_first_name)s);
                """,
                {
                    'new_user_chat_id': chat_id,
                    'new_user_first_name': first_name
                }
            )

    def change_location_for_user(self,chat_id, city, country):
        """Set/Change city and country for user and drop old city's id"""
        with self.connection:
            self.cursor.execute(
                """
                UPDATE users
                SET city = %(city)s, country = %(country)s, city_id = NULL
                WHERE chat_id = %(chat_id)s;
                """,
                {
                    'city': city,
                    'country': country,
                    'chat_id': chat_id
                }
            )

    def update_city_id_for_user(self, chat_id, city_id):
        """Set new city_id in DB"""
        with self.connection:
            self.cursor.execute(
                """
                UPDATE users
                SET city_id = %(city_id)s
                WHERE chat_id = %(chat_id)s;
                """,
                {
                    'city_id': city_id,
                    'chat_id': chat_id
                }
            )

    def close(self):
        """Close the connection with DB"""
        self.connection.close()
