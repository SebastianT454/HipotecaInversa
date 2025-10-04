# Importing to include the search path
import sys
sys.path.append("src")
sys.path.append(".")

import psycopg2
import os
from psycopg2 import sql
from controller import Secret_Config
from model.User import User

# CONSTANTS
# Maximum age allowed
MAX_LIFE_EXPECTANCY_MALES = 84
MAX_LIFE_EXPECTANCY_FEMALES = 86

# Minimum age allowed
MIN_AGE = 62

# Minimum property value
MIN_PROPERTY_VALUE = 10000000

# Maximum and minimum interest rates allowed
MIN_INTEREST_RATE = 6
MAX_INTEREST_RATE = 43


# EXCEPTIONS
class ClientNotUpdatedException(Exception):
    """ 
    Custom exception for when the client cannot be updated
    """
    def __init__(self):
        super().__init__("The client could not be updated")

class ClientNotInsertedException(Exception):
    """ 
    Custom exception for when the client cannot be inserted into the table
    """
    def __init__(self):
        super().__init__("The client could not be inserted")

class ClientNotDeletedException(Exception):
    """ 
    Custom exception for when the client cannot be deleted from the table
    """
    def __init__(self):
        super().__init__("The client could not be deleted")

class AgeException(Exception):
    """ 
    Custom exception for age below minimum or above maximum
    """
    def __init__(self, age):
        super().__init__(f"The age: {age} is invalid; to apply for a reverse mortgage, one must be between {MIN_AGE} and {MAX_LIFE_EXPECTANCY_MALES}")

class NoneException(Exception):
    """ 
    Custom exception for None values
    """
    def __init__(self):
        super().__init__("There cannot be empty fields")

class PropertyValueException(Exception):
    """ 
    Custom exception for property values below the minimum
    """
    def __init__(self):
        super().__init__("Property value cannot be below the minimum")

class InterestRateException(Exception):
    """ 
    Custom exception for interest rates above the maximum, below the minimum, and zero
    """
    def __init__(self, interest_rate):
        super().__init__(f"The interest rate: {interest_rate} is invalid; it should not be less than {MIN_INTEREST_RATE} or greater than {MAX_INTEREST_RATE}")


class ClientController:

    @staticmethod
    def get_cursor():
        """
        Creates a connection to the database and returns it
        """
        DATABASE = Secret_Config.PGDATABASE
        USER = Secret_Config.PGUSER
        PASSWORD = Secret_Config.PGPASSWORD
        HOST = Secret_Config.PGHOST
        PORT = Secret_Config.PGPORT
        print(DATABASE,USER,PASSWORD,HOST,PORT)
        # Connecting to the database
        connection = psycopg2.connect( database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT )
        return connection.cursor()

    @staticmethod
    def create_table():
        """
        Creeates user table if it doesn't exist.
        """    
        # Obtener el directorio actual del archivo (src/controller/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Subir dos niveles: src/controller -> src -> backend
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        # Construir ruta al archivo SQL
        sql_path = os.path.join(base_dir, 'sql', 'crear_usuarios.sql')
        
        print(f"Buscando archivo SQL en: {sql_path}")  # Para debug
        
        with open(sql_path, "r") as f:
            sql = f.read()

        cursor = ClientController.get_cursor()
        try:
            cursor.execute( sql )
            cursor.connection.commit()
        except:
            # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
            cursor.connection.rollback()

    @staticmethod
    def clear_table():
        """ 
        Deletes all records from the clients table in the database 
        """
        cursor = ClientController.get_cursor()

        # Execute the query to delete all records from the table
        cursor.connection.commit()
        cursor.close()
        cursor.connection.close()
        
    @staticmethod
    def insert_client(client: User):
        """ 
        Receives an instance of the User class and inserts it into the respective table
        """
        cursor = ClientController.get_cursor()

        ClientController.verify_empty_fields(client.id, client.marital_status, client.age, client.property_value, client.interest_rate)
        ClientController.verify_age(int(client.age))
        ClientController.verify_property(float(client.property_value))
        ClientController.verify_interest(float(client.interest_rate))

        try:
            # Conditional to check if the client has a spouse
            if client.marital_status.title() in ["Married", "Wedded","Casado","Casada"]: 
                # Para usuarios casados
                cursor.execute(
                    sql.SQL("""
                        INSERT INTO users (id, age, gender, marital_status, spouse_age, spouse_gender, property_value, interest_rate)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """),
                    (client.id, client.age, client.gender, client.marital_status, client.spouse_age, client.spouse_gender, client.property_value, client.interest_rate)
                )
            else:
                # Insertar si esta soltero
                cursor.execute(
                    sql.SQL("""
                        INSERT INTO users (id, age, gender, marital_status, property_value, interest_rate)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """),
                    (client.id, client.age, client.gender, client.marital_status, client.property_value, client.interest_rate)
                )

            cursor.connection.commit()
            
        except Exception as e:
            cursor.connection.rollback()
            print(f"Error agregando usuario: {e}")
            raise ClientNotInsertedException()
        finally:
            cursor.close()
            cursor.connection.close()
    
    @staticmethod
    def find_client(id):
        """ 
        Fetches a client from the clients table by ID number 
        """
        cursor = ClientController.get_cursor()

        try:
            # Using sql.SQL for query
            cursor.execute(
                sql.SQL("""
                    SELECT id, age, gender, marital_status, spouse_age, spouse_gender, property_value, interest_rate
                    FROM users WHERE id = %s
                """),
                (id,)
            )

            row = cursor.fetchone()
            if row:
                result = User(id=row[0], age=row[1], gender=row[2], marital_status=row[3], spouse_age=row[4],
                            spouse_gender=row[5], property_value=row[6], interest_rate=row[7])
                return result
            else:
                return None
        except Exception as e:
            print(f"Error finding client: {e}")
            return None
        finally:
            cursor.close()
            cursor.connection.close()
    
    @staticmethod
    def delete_client(id):
        """ 
        Deletes a client from the Clients table
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(sql.SQL("DELETE FROM users WHERE id = %s"), (id,))
            cursor.connection.commit()
        except Exception as e:
            print(f"Error deleting client: {e}")
            raise ClientNotDeletedException()
        finally:
            cursor.close()
            connection.close()
             
    @staticmethod
    def update_client(id, updated_data: User):
        """ 
        Updates the values of a client in the clients table by ID number
        """
        cursor = ClientController.get_cursor()

        try:
            # Actualiza el ID del cliente
            if updated_data.id:
                cursor.execute(
                    sql.SQL("UPDATE users SET id = %s WHERE id = %s"),
                    (updated_data.id, id)
                )

            # Actualiza estado civil y datos del cónyuge
            if updated_data.marital_status:
                if updated_data.marital_status.title() == "Married":  
                    cursor.execute(
                        sql.SQL("UPDATE users SET marital_status = %s, spouse_age = %s, spouse_gender = %s WHERE id = %s"),
                        (updated_data.marital_status, updated_data.spouse_age, updated_data.spouse_gender, id)
                    ) 
                else:
                    cursor.execute(
                        sql.SQL("UPDATE users SET marital_status = 'Single', spouse_age = NULL, spouse_gender = NULL WHERE id = %s"),
                        (id,)
                    )

            
            # Actualiza valor de la propiedad
            if updated_data.property_value:
                cursor.execute(
                    sql.SQL("UPDATE users SET property_value = %s WHERE id = %s"),
                    (updated_data.property_value, id)
                )

            # Actualiza tasa de interés
            if updated_data.interest_rate:
                cursor.execute(
                    sql.SQL("UPDATE users SET interest_rate = %s WHERE id = %s"),
                    (updated_data.interest_rate, id)
                )

            # Hacer commit una sola vez al final
            cursor.connection.commit()

        except Exception as e:
            print(f"Error updating client: {e}")
            raise ClientNotUpdatedException()
        finally:
            cursor.close()
            cursor.connection.close()

        
    @staticmethod
    def verify_empty_fields(id, marital_status, age, property_value, interest_rate):
        if id is None or marital_status is None or age is None or property_value is None or interest_rate is None:
            raise NoneException()

    @staticmethod
    def verify_age(age):
        if age < MIN_AGE or age > MAX_LIFE_EXPECTANCY_MALES:
            raise AgeException(age)
        
    @staticmethod
    def verify_property(property_value):
        if property_value < MIN_PROPERTY_VALUE:
            raise PropertyValueException()
    
    @staticmethod
    def verify_interest(interest_rate):
        if interest_rate < MIN_INTEREST_RATE or interest_rate > MAX_INTEREST_RATE:
            raise InterestRateException(interest_rate)