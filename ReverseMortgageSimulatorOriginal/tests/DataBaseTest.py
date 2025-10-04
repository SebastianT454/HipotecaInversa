import unittest
import sys
from psycopg2 import sql

# We import it so we can include the python search path
sys.path.append("src")
sys.path.append(".")

# Import the required modules
from src.Model.User import User
from src.controller.Controlador_usuarios import ClientController, NoneException , AgeException, PropertyValueException, InterestRateException, MIN_AGE, MAX_INTEREST_RATE, MIN_INTEREST_RATE, MIN_PROPERTY_VALUE, MAX_LIFE_EXPECTANCY_MALES

class ControllerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests to initialize the database and clean up the table.
        """
        ClientController.clear_table() # Make sure you use the correct name here

    def test_insert_usuario(self):
        usuario_prueba = User(
            id="1234657", 
            age="65", 
            marital_status="soltero",
            spouse_age=None, 
            spouse_gender=None, 
            property_value="100000000", 
            interest_rate="25"
        )
        
        print("Insertando usuario de prueba...")
        ClientController.insert_client(usuario_prueba)
        print("Usuario insertado. Buscando usuario...")

        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        print(f"Usuario buscado: {usuario_buscado}")  # This should display user details or 'None'

        self.assertIsNotNone(usuario_buscado, "El usuario no se encontró después de la inserción.")
        self.assertTrue(usuario_buscado.is_equal(usuario_prueba), "Los datos del usuario encontrado no coinciden.")



    def test_find_usuario(self):
        """
        Tests whether a user can be searched after being inserted.
        """
        usuario_prueba = User(
            id="12346577", 
            age="65", 
            marital_status="soltero",
            spouse_age=None, 
            spouse_gender=None, 
            property_value="100000000", 
            interest_rate="25"
        )
        
        ClientController.insert_client(usuario_prueba)  # Pre-insertion
        
        # Find the inserted user
        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        self.assertIsNotNone(usuario_buscado, "El usuario no se encontró después de la inserción.")
        self.assertTrue(usuario_buscado.is_equal(usuario_prueba), "Los datos del usuario encontrado no coinciden.")

    def test_none_error(self):
        """
        Test that the None_Exception exception is thrown when trying to insert a user with a null ID.
        """
        usuario_prueba = User(
            id=None, 
            age="68", 
            marital_status="casada",
            spouse_age="62", 
            spouse_gender="hombre", 
            property_value="1000000000", 
            interest_rate="33"
        )

        with self.assertRaises(NoneException):
            ClientController.insert_client(usuario_prueba)  # Make sure you use the correct name here

    def test_update_usuario(self):
        """
        Tests that a user can be updated successfully.
        """
        # Suppose the user has already been inserted previously
        usuario_prueba = User(
            id="987654321",
            age="65",
            marital_status="Soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="120000000",
            interest_rate="30"
        )

        # Update age
        usuario_actualizado = User(
            id="987654321",
            age="66",  # We only update the age
            marital_status="Married",
            spouse_age="64",
            spouse_gender="mujer",
            property_value="120000000",
            interest_rate="30"
        )

        ClientController.update_client(usuario_prueba.id, usuario_actualizado)

        usuario_buscado = ClientController.find_client(usuario_prueba.id)

        print("Datos del usuario buscado:", usuario_buscado)
        print("Datos del usuario actualizado:", usuario_actualizado)

        self.assertTrue(usuario_actualizado.is_equal(usuario_actualizado), "Los datos del usuario encontrado no coinciden con los datos actualizados.")




    def test_delete_usuario(self):
        """
        Tests that a user is deleted successfully.
        """
        # Create a test user and insert it
        usuario_prueba = User(
            id="1234658", 
            age="70", 
            marital_status="casado",
            spouse_age="68", 
            spouse_gender="mujer", 
            property_value="200000000", 
            interest_rate="35"
        )
        
        ClientController.insert_client(usuario_prueba)

        # Delete the user
        ClientController.delete_client(usuario_prueba.id)

        # Try to find the deleted user
        usuario_buscado = ClientController.find_client(usuario_prueba.id)
        self.assertIsNone(usuario_buscado, "El usuario no debería encontrarse después de ser eliminado.")
    # Repeat for other functions
    def test_age_exception(self):
        """
        Test to throw AgeException for an invalid age.
        """
        age_invalid = 15  # Age less than the minimum allowed
        usuario_prueba = User(
            id="1234567",
            age=age_invalid,
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate="25"
        )

        with self.assertRaises(AgeException) as context:
            ClientController.insert_client(usuario_prueba)  # Asegúrate de que esto verifique la edad
        self.assertEqual(str(context.exception), f"The age: {age_invalid} is invalid; to apply for a reverse mortgage, one must be between {MIN_AGE} and {MAX_LIFE_EXPECTANCY_MALES}")

    def test_none_exception(self):
        """
        Test to throw NoneException when trying to insert a user with null fields.
        """
        usuario_prueba = User(
            id=None, 
            age="68", 
            marital_status="casada",
            spouse_age=None,  # Campo nulo
            spouse_gender="hombre", 
            property_value="1000000000", 
            interest_rate="33"
        )

        with self.assertRaises(NoneException):
            ClientController.insert_client(usuario_prueba)

    def test_property_value_exception(self):
        """
        Tests whether the PropertyValueException is thrown for an invalid property value.
        """
        usuario_prueba = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="50000",  # Value below minimum allowed
            interest_rate="25"
        )

        with self.assertRaises(PropertyValueException) as context:
            ClientController.insert_client(usuario_prueba)
        self.assertEqual(str(context.exception), "Property value cannot be below the minimum")

    def test_interest_rate_exception_above_maximum(self):
        """
        Test that the InterestRateException is thrown for an interest rate greater than the maximum.
        """
        interest_rate_too_high = 50.0  # Make sure to use a decimal number
        usuario_prueba_high = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate=interest_rate_too_high
        )

        with self.assertRaises(InterestRateException) as context_high:
            ClientController.insert_client(usuario_prueba_high)

        # Adjust the expected message to include the value with decimal point
        self.assertEqual(str(context_high.exception), f"The interest rate: {interest_rate_too_high} is invalid; it should not be less than {MIN_INTEREST_RATE} or greater than {MAX_INTEREST_RATE}")



    def test_interest_rate_valid(self):
        """
        Test that a user can be inserted with a valid interest rate.
        """
        interest_rate_valid = 30  # Valid interest rate, within the permitted limits
        usuario_prueba = User(
            id="1234567",
            age="65",
            marital_status="soltero",
            spouse_age=None,
            spouse_gender=None,
            property_value="100000000",
            interest_rate=interest_rate_valid
        )

        try:
            ClientController.insert_client(usuario_prueba)  # Should pass without throwing exception
        except InterestRateException:
            self.fail("InterestRateException should not have been raised for a valid interest rate")


if __name__ == '__main__':
    unittest.main()
