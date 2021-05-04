""" Graphql Address Schema Module """
import requests
import xmltodict

from graphene import (Interface, String, ObjectType, Connection)
from app import (PO_URL, PO_USERID)
from .helpers import TotalCount


def postal_code_request(postal_code):
    """API call to USPS system to retrieve city state based on zip code."""
    url = '{}?API=CityStateLookup&XML=<CityStateLookupRequest USERID="{}">' \
          '<ZipCode ID=\'0\'><Zip5>{}</Zip5></ZipCode>'  \
          '</CityStateLookupRequest>'.format(PO_URL, PO_USERID,
                                             postal_code)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["CityStateLookupResponse"]["ZipCode"]
        if 'Error' in response:
            return {'error': response['Error']['Description']}
        return {'postalcode': postal_code, 'city': response["City"],
                'state': response["State"]}

    return None

def verify_address_request(postal_code, address1, address2, city, state):
    """API call to USPS system to verify address against zip code."""
    url = '{}?API=Verify&XML=<AddressValidateRequest USERID="{}">' \
        '<Address><Address1>{}</Address1><Address2>{}</Address2>' \
        '<City>{}</City><State>{}</State><Zip5>{}</Zip5><Zip4></Zip4>' \
        '</Address></AddressValidateRequest>'.format(PO_URL, PO_USERID,
                                                     address2, address1,
                                                     city, state,
                                                     postal_code)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["AddressValidateResponse"] \
                                                ["Address"]
        if 'Error' in response:
            return {'error': response['Error']['Description']}

        if 'Zip4' in response:
            postal_code = '{}-{}'.format(response['Zip5'], response['Zip4'])
        else:
            postal_code = response['Zip5']
# API uses Address2 as the primary address field
        if 'Address1'in response:
            address1 = response['Address1']
            address2 = response['Address2']
        else:
            address1 = response['Address2']
            address2 = None

        return {'postalcode': postal_code, 'city': response["City"],
                'state': response["State"], 'address1': address1,
                'address2': address2}

    return {'postalcode': None, 'city': None, 'state': None,
            'address1': None, 'address2': None}

def resolve_address(parent, info, postalcode, address1, address2='',
                    city='', state=''):
    """ Verify / cleanup address based on USPS information. """
    address = verify_address_request(postalcode, address1, address2, city,
                                     state)
    return Address(
        postalcode=postalcode,
        city=address['city'],
        state=address['state'],
        address1=address['address1'],
        address2=address['address2']
    )


def resolve_city_states(parent, info, postalcode):
    """ Get city / state from USPS based on zip code. """
    city_state = postal_code_request(postalcode)
    return CityState(
        postalcode=postalcode,
        city=city_state['city'],
        state=city_state['state']
    )

class Address(ObjectType):
    """ Address fields output """
    postalcode = String()
    city = String()
    state = String()
    address1 = String()
    address2 = String()


class CityState(ObjectType):
    """ City State fields output """
    postalcode = String()
    city = String()
    state = String()


class AddressNode(ObjectType):
    """ Address Graphql Node output """
#    class Meta:
#        """ Address Graphql Node output """
#        interfaces = (Address,)

    postalcode = String()
    city = String()
    state = String()
    address1 = String()
    address2 = String()


class AddressConnection(Connection):
    """ Address Graphql Query output """
    class Meta:
        """ Address Graphql Query output """
        node = AddressNode
        interfaces = (TotalCount,)


class CityStateNode(ObjectType):
    """ CityStateGraphql Node output """
#    class Meta:
#        """ CityState Graphql Node output """
#        interfaces = (CityState,)

    postalcode = String()
    city = String()
    state = String()

class CityStateConnection(Connection):
    """ CityState Graphql Query output """
    class Meta:
        """ CityState Graphql Query output """
        node = CityStateNode
        interfaces = (TotalCount,)
