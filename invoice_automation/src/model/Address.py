class Address:
    """
    Model for addresses
    Inputted by schools during registration
    """
    def __init__(self, line1: str, line2: str, city: str, state: str, country: str, zipCode: str):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.state = state
        self.country = country
        self.zipCode = zipCode