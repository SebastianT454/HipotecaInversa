class ClientException(Exception):
    """
    Base class for all client-related exceptions.
    This exception is used for errors related to invalid client information.
    """
    pass


class ReverseMortgageException(Exception):
    """
    Base class for all reverse mortgage-related exceptions.
    This exception is used for errors related to reverse mortgage calculations or constraints.
    """
    pass


class NegativeInterest(ReverseMortgageException):
    """
    Raised when a negative interest rate is encountered.
    Reverse mortgages should not have negative interest rates.
    """
    pass


class AboveMaxInterest(ReverseMortgageException):
    """
    Raised when an interest rate exceeds the maximum allowable rate.
    Reverse mortgages have a maximum interest rate limit.
    """
    pass


class NegativePropertyValue(ReverseMortgageException):
    """
    Raised when a negative property value is provided.
    Property values must be positive for reverse mortgage calculations.
    """
    pass


class PropertyZeroValue(ReverseMortgageException):
    """
    Raised when a zero property value is provided.
    A property value of zero is invalid for reverse mortgage calculations.
    """
    pass


class NegativeAge(ClientException):
    """
    Raised when a negative age is provided for a client.
    Client age must be a positive integer.
    """
    pass


class AboveMaxAge(ClientException):
    """
    Raised when a client's age exceeds the maximum allowable age.
    There is typically an upper limit for age in client-related calculations or constraints.
    """
    pass


class BelowMinAge(ClientException):
    pass


class InvalidAge(ClientException):
    """
    Raised when an invalid age value is provided.
    Age must be a valid positive integer within acceptable ranges.
    """
    pass


class InvalidGender(ClientException):
    """
    Raised when an invalid gender value is provided.
    Gender must be specified in an acceptable format.
    """
    pass


class InvalidMaritalStatus(ClientException):
    """
    Raised when an invalid marital status value is provided.
    Marital status must be specified in an acceptable format.
    """
    pass


class Client:
    """
    Class representing a client for the reverse mortgage.

    Clase que representa un cliente para la hipoteca inversa.
    """

    def __init__(self, age: int, gender: str, marital_status: str, spouses_age: int | None, spouses_gender: str | None):
        """
        Initializes the client with personal details and calculates derived attributes.

        Inicializa al cliente con detalles personales y calcula atributos derivados.

        Parameters
        ----------
        age : int
            The age of the client / Edad del cliente
        gender : str
            The gender of the client, expected to be 'M' or 'F' / Género del cliente, se espera 'M' o 'F'
        marital_status : str
            The marital status of the client, expected to be one of 'married', 'single', 'widowed', or 'divorced' / Estado civil del cliente, se espera uno de 'married', 'single', 'widowed' o 'divorced'
        spouses_age : int | None
            The age of the spouse if married, otherwise None / Edad del cónyuge si está casado, de lo contrario None
        spouses_gender : str | None
            The gender of the spouse if married, otherwise None / Género del cónyuge si está casado, de lo contrario None
        """
        self.age = age
        self.gender = gender
        self.marital_status = marital_status
        self.spouses_age = spouses_age
        self.spouses_gender = spouses_gender
        self.minor_age = self.check_minor_age()
        self.minor_gender = self.check_minor_gender()
        self.estimated_years_of_life = self.calculate_years_of_life()

    def check_valid_age(self):
        """
        Checks the validity of the client's age and spouse's age if applicable.

        Verifica la validez de la edad del cliente y la edad del cónyuge si aplica.
        """
        max_male_age_allowed = 74
        max_female_age_allowed = 79

        if type(self.age) != int:
            raise InvalidAge(f'Age ({self.age}) is not a valid number')

        if self.age < 0:
            raise NegativeAge(f'Age ({self.age}) can not be negative')
        elif self.age == 0:
            raise InvalidAge(f'Age can not be zero')
        elif self.gender.lower() == 'm' and self.age > max_male_age_allowed:
            raise AboveMaxAge(f'Age ({self.age}) is greater than the maximum age allowed for males ({max_male_age_allowed})')
        elif self.gender.lower() == 'f' and self.age > max_female_age_allowed:
            raise AboveMaxAge(f'Age ({self.age}) is greater than the maximum age allowed for females ({max_female_age_allowed})')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_age < 0:
                raise NegativeAge(f'Age ({self.spouses_age}) can not be negative')
            elif self.spouses_age == 0:
                raise InvalidAge(f'Spouse\'s age can not be zero')
            elif self.spouses_gender.lower() == 'm' and self.spouses_age > max_male_age_allowed:
                raise AboveMaxAge(f'Age ({self.spouses_age}) is greater than the maximum age allowed for males ({max_male_age_allowed})')
            elif self.spouses_gender.lower() == 'f' and self.spouses_age > max_female_age_allowed:
                raise AboveMaxAge(f'Age ({self.spouses_age}) is greater than the maximum age allowed for females ({max_female_age_allowed})')

    def check_valid_gender(self):
        """
        Checks the validity of the client's gender and spouse's gender if applicable.

        Verifica la validez del género del cliente y el género del cónyuge si aplica.
        """
        available_genders = ['m', 'f']
        if self.gender.lower() not in available_genders:
            raise InvalidGender(f'Gender ({self.gender}) is not valid, only "M" or "F" allowed')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_gender.lower() not in available_genders:
                raise InvalidGender(f'Spouses gender ({self.spouses_gender}) is not valid')

    def check_valid_marital_status(self):
        """
        Checks the validity of the client's marital status.

        Verifica la validez del estado civil del cliente.
        """
        available_marital_status = ['married', 'single', 'widowed', 'divorced']
        if self.marital_status.lower() not in available_marital_status:
            raise InvalidMaritalStatus(f'Marital status ({self.marital_status}) is not valid, only married, single, widowed or divorced allowed')

    def check_minor_age(self):
        """
        Determines the minimum age between the client and spouse if married.

        Determina la edad mínima entre el cliente y el cónyuge si está casado.
        """
        self.check_valid_age()
        self.check_valid_marital_status()

        if self.marital_status.lower() != "married" or self.age <= self.spouses_age:
            return self.age
        else:
            return self.spouses_age

    def check_minor_gender(self):
        """
        Determines the gender associated with the minimum age.

        Determina el género asociado con la edad mínima.
        """
        self.check_valid_gender()
        self.check_valid_marital_status()
        if self.marital_status.lower() != "married" or self.minor_age == self.age:
            return self.gender
        else:
            return self.spouses_gender

    def calculate_years_of_life(self):
        """
        Calculates the estimated years of life based on the minimum age and gender.

        Calcula los años estimados de vida en función de la edad mínima y el género.
        """
        male_life_expect = 75
        female_life_expect = 80
        min_age_allowed = 60

        self.check_valid_age()
        self.check_valid_gender()

        if self.minor_age < min_age_allowed:
            raise InvalidAge(f'Age of younger person is lesser than minimum age allowed ({min_age_allowed})')

        if self.minor_gender.lower() == "m":
            return male_life_expect - self.minor_age
        
        elif self.minor_gender.lower() == "f":
            return female_life_expect - self.minor_age

    def __repr__(self) -> str:
        """
        Returns a string representation of the client information.

        Devuelve una representación en cadena de la información del cliente.
        """
        if self.marital_status.lower() == "married":
            return f'Age: {self.age} \nGender: {self.gender.upper()} \nMarital Status: {self.marital_status.title()} \n\nSpouse\'s Age: {self.spouses_age} \nSpouse\'s Gender: {self.spouses_gender.upper()}'
        else:
            return f'Age: {self.age} \nGender: {self.gender.upper()} \nMarital Status: {self.marital_status.title()}'


class ReverseMortgage:
    """
    Class representing a reverse mortgage for a client.

    Clase que representa una hipoteca inversa para un cliente.
    """

    def __init__(self, property_value: int, interest: float, client: Client):
        """
        Initializes the reverse mortgage with property value, interest rate, and client details.

        Inicializa la hipoteca inversa con el valor de la propiedad, la tasa de interés y los detalles del cliente.

        Parameters
        ----------
        property_value : int
            The value of the property / Valor de la propiedad
        interest : float
            The annual interest rate for the reverse mortgage / Tasa de interés anual para la hipoteca inversa
        client : Client
            The client applying for the reverse mortgage / El cliente que solicita la hipoteca inversa
        """
        self.property_value = property_value
        self.interest = interest
        self.client = client
        self.quotas = self.calculate_quotas()
        self.monthly_rate = self.calculate_monthly_rate()

    def check_valid_property_value(self):
        """
        Checks the validity of the property value.

        Verifica la validez del valor de la propiedad.
        """
        if self.property_value < 0:
            raise NegativePropertyValue(f'Property value {self.property_value} can not be negative')
        elif self.property_value == 0:
            raise PropertyZeroValue(f'Property value {self.property_value} can not be zero')

    def check_valid_interest(self):
        """
        Checks the validity of the interest rate.

        Verifica la validez de la tasa de interés.
        """
        max_interest = 8
        if self.interest < 0:
            raise NegativeInterest(f'Interest {self.interest} can not be negative')
        elif self.interest > max_interest:
            raise AboveMaxInterest(f'Interest {self.interest} can not be above {max_interest}')

    def calculate_quotas(self):
        """
        Calculates the number of monthly payments based on the client's estimated years of life.

        Calcula el número de pagos mensuales en función de los años estimados de vida del cliente.
        """
        return self.client.estimated_years_of_life * 12

    def calculate_monthly_rate(self):
        """
        Calculates the monthly interest rate from the annual interest rate.

        Calcula la tasa de interés mensual a partir de la tasa de interés anual.
        """
        self.check_valid_interest()

        if self.interest == 0:
            return 0
        
        annual_rate = self.interest / 100
        monthly_rate = (1 + annual_rate) ** (1 / 12) - 1
        return monthly_rate

    def calculate_monthly_fee(self):
        """
        Calculates the monthly fee based on the property value, interest rate, and number of quotas.

        Calcula la cuota mensual en función del valor de la propiedad, la tasa de interés y el número de cuotas.
        """
        self.check_valid_interest()
        self.check_valid_property_value()

        if self.interest == 0:
            return round(self.property_value / self.quotas, 2)
        
        numerator = self.property_value * self.monthly_rate * (1 + self.monthly_rate) ** self.quotas
        denominator = ((1 + self.monthly_rate) ** self.quotas) - 1
        monthly_fee = numerator / denominator
        
        return round(monthly_fee, 2)

    def __repr__(self) -> str:
        """
        Returns a string representation of the reverse mortgage details.

        Devuelve una representación en cadena de los detalles de la hipoteca inversa.
        """
        return f'Property Value: ${self.property_value:,} \nInterest: {self.interest}% \nQuotas: {self.quotas} \nMonthly Rate: {round(self.monthly_rate, 6)} \n\nMonthly Fee: ${self.calculate_monthly_fee():,}'
