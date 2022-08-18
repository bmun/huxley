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
    country_sub_division_code: str
        Country_sub_division_code of address, corresponds to state/region
    country: str
        Country of address
    zip_code: str
        Zip code of address
    """

    def __init__(self, line1: str, line2: str, city: str, country_sub_division_code: str, country: str, zip_code: str):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.country_sub_division_code = country_sub_division_code
        self.country = country
        self.zip_code = zip_code
