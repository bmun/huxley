# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json


class Constants():
    '''Base class that allows constants to be serialized to JSON.'''

    @classmethod
    def to_dict(cls):
        return {k: v for k, v in vars(cls).items() if not k.startswith('__')}

    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict())


class ContactGender(Constants):
    '''Gender of a school's primary/secondary contacts.'''
    MALE = 1
    FEMALE = 2
    OTHER = 3
    UNSPECIFIED = 4


class ContactType(Constants):
    '''Whether a school's primary/secondary contact is a student or faculty.'''
    STUDENT = 1
    FACULTY = 2


class ProgramTypes(Constants):
    '''Type of a school's MUN program.'''
    CLUB = 1
    CLASS = 2


class PaymentTypes(Constants):
    '''Type of a payment method'''
    CARD = 1
    CHECK = 2

class StateTypes(Constants):
    '''Which state a school is from.'''
    ALABAMA = "AL"
    ALASKA = "AK"
    AMERICAN_SAMOA = "AS"
    ARIZONA = "AZ"
    ARKANSAS = "AR"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DELAWARE = "DE"
    DISTRICT_OF_COLUMBIA = "DC"
    FLORIDA = "FL"
    GEORGIA = "GA"
    GUAM = "GU"
    HAWAII = "HI"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    IOWA = "IA"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MAINE = "ME"
    MARYLAND = "MD"
    MASSACHUSETTS = "MA"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSISSIPPI = "MS"
    MISSOURI = "MO"
    MONTANA = "MT"
    NEBRASKA = "NE"
    NEVADA = "NV"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    NORTHERN_MARIANA_IS = "MP"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    PUERTO_RICO = "PR"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VERMONT = "VT"
    VIRGINIA = "VA"
    VIRGIN_ISLANDS = "VI"
    WASHINGTON = "WA"
    WEST_VIRGINIA = "WV"
    WISCONSIN = "WI"
    WYOMING = "WY"
