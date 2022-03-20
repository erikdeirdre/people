""" Graphql Address Schema Module """
import requests
import xmltodict
import logging

from graphene import (String, ObjectType, Connection)
from app import (PO_URL, PO_USERID)
from .helpers import TotalCount

logger = logging.getLogger(__name__)

def postal_code_request(postal_code):
    """API call to USPS system to retrieve city state based on zip code."""
    url = f'{PO_URL}?API=CityStateLookup&XML=<CityStateLookupRequest USERID="{PO_USERID}">' \
          f'<ZipCode ID=\'0\'><Zip5>{postal_code}</Zip5></ZipCode>'  \
          f'</CityStateLookupRequest>'
    
    with open("url.txt", "w") as u:
        u.write(url)
    u.close()
    logger.debug(url)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["CityStateLookupResponse"]["ZipCode"]
        if 'Error' in response:
            logger.error(f"Error processing {postal_code}")
            return {'error': response['Error']['Description']}
        logger.debug(f"Successfully process postal code, {postal_code}."
                     f"data: {response['City']}, {response['State']}")
        return {'postalcode': postal_code, 'city': response["City"],
                'state': response["State"]}
    else:
        logger.error(f"Error processing postal code: {postal_code},"
                     f"rc: {results.status_code}")
        return None

def verify_address_request(postal_code, address1, address2=None, city=None,
                           state=None):
    """API call to USPS system to verify address against zip code."""
    url = f'{PO_URL}?API=Verify&XML=<AddressValidateRequest USERID="{PO_USERID}">' \
        f'<Address><Address1>{address1}</Address1><Address2>{address2}</Address2>' \
        f'<City>{city}</City><State>{state}</State><Zip5>{postal_code}</Zip5>' \
        f'<Zip4></Zip4></Address></AddressValidateRequest>'

    logger.debug(url)

    results = requests.get(url)
    if results.status_code == 200:
        response = xmltodict.parse(results.text)["AddressValidateResponse"] \
                                                ["Address"]
        if 'Error' in response:
            logger.error(f"Error processing postal code, {postal_code}"
                         f" address, {address1}")
            return {'error': response['Error']['Description']}

        if 'Zip4' in response:
            postal_code = f"{response['Zip5']}-{response['Zip4']}"
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
    return AddressNode(
        postalcode=postalcode,
        city=address['city'],
        state=address['state'],
        address1=address['address1'],
        address2=address['address2']
    )


def resolve_city_states(parent, info, postalcode):
    """ Get city / state from USPS based on zip code. """
    city_state = postal_code_request(postalcode)
    return CityStateNode(
        postalcode=postalcode,
        city=city_state['city'],
        state=city_state['state']
    )


class AddressNode(ObjectType):
    """ Address Graphql Node output """
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
    postalcode = String()
    city = String()
    state = String()

class CityStateConnection(Connection):
    """ CityState Graphql Query output """
    class Meta:
        """ CityState Graphql Query output """
        node = CityStateNode
        interfaces = (TotalCount,)
