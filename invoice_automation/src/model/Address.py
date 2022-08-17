class Address:
    """
    Model for addresses
    Inputted by schools during registration

    Attributes
    ----------
    line1: str
        First line of address
    line2: str
        Second line of address, empty string if blank
    city: str
        City of address
    countrySubDivisionCode: str
        CountrySubDivisionCode of address, corresponds to state/region
    country: str
        Country of address
    zipCode: str
        Zip code of address
    """

    def __init__(self, line1: str, line2: str, city: str, countrySubDivisionCode: str, country: str, zipCode: str):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.countrySubDivisionCode = countrySubDivisionCode
        self.country = country
        self.zipCode = zipCode
