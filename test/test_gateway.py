# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import fatzebra

# Setup some test details
VALID_CARD = '5123456789012346'
DECLINED_CARD = '4242424242424242'
INVALID_CARD = '5123456789012345'

NOW = datetime.datetime.now()
VALID_EXPIRY = "%d/%d" % (NOW.month, NOW.year + 4)

class FatZebraTestCase(unittest.TestCase):
    def setUp(self):
        super(FatZebraTestCase, self).setUp()

class FatZebraGatewayTest(FatZebraTestCase):
    def test_gateway_sets_parameters_properly(self):
        gateway = fatzebra.gateway.Gateway("Franks", "Beans")
        self.assertEqual(gateway.username, "Franks")
        self.assertEqual(gateway.token, "Beans")

    def test_uri_is_built_properly(self):
        gateway = fatzebra.gateway.Gateway("TEST", "TEST", False)
        self.assertEqual(
            gateway._uri(), "https://gateway.fatzebra.com.au/v1.0/purchases")

    def test_purchase_works(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.purchase(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(result.successful)

    @staticmethod
    def __serialize_fraud_payload(customer_type, shipping_type):
        """Serialize the fraud payload. ReD has 3 different response types: Accept, Challenge, Deny.
        It accepts the following emails for testing: {accept, challenge, deny}@email.com

        Based on this, customer_type and shipping_type are two params passed as one of those emails,
        such as; customer_type: accept@email.com and shipping_type: deny@email.com
        For the same responses, response_type1 and response_type2 are set to same.

        :param customer_type: Either accept, challenge or deny for customer payload.
        :param shipping_type: Either accept, challenge or deny for shipping_address payload.
        :return: Payload
        """
        payload = {
            "customer": {
                "address_1": "23 Smith Road",
                "city": "Canberra",
                "country": "AUS",
                "created_at": datetime.datetime.utcnow().isoformat(),
                "email": "{0}@email.com".format(customer_type),
                "existing_customer": True,
                "first_name": "James",
                "last_name": "Smith",
                "id": "ABD123",
                "post_code": "2600"
            },
            "device_id": "04003hQUMXGB0poNf94lis1ztjiCqvcbsN56bsuwsjuElyNu8BhUMCZzxJu5KaKrVRoPks+Sl5kZMVA4D1yzhjUZHdETNKeMs9+YWgT+Kx4Epa0/yoVIBnjain3l6hbzqbSTjyylda8tv/p+hOVDTbnr7BCIp0wtRbmoh0ylJGfM1m5dSDvFsQ9SoXAEKkoBeycPTld6LUiJXX9c8V1ZIWK++ykzCGBlggcGImwI4pTgqhbiV4XFveMqjhKePA1UZdKAZDwic+y5/r+SkyAbziDM7k8xAXTS4l7D1erHMnjL6riE+V79BTuQujkd6ANXzYbYiVcAZxPGQ1+WMCVbBcdxP6GA3q0kDinWcD6T1dGUjL/YgLUkuWAapecJ9jsJ+bfNdWTfYwpMVz5nPnl/jsrGjhHT5S5MgyzBqMl2d7573o/ED3HepEpuM5tlG61Ntm9z3eln9a65pRCiBordUO6M2UtezWwdrLOsKoxk0tBb1QXpA0h4C+tFNeowfmZjGrzuOZ8GLqXVxfWKXTaqUhFUi4FfJwjCz3bq72B5V9rdDiApQs/EGzmZL5HExNzY4wQ1n6+4nxW5nei2EMlMtbRnNwQxSxzPuRtycb0H5IjHkCcKSs4KVYKB4vaBnQE/NFveVlaPFRfz06FHDo0vYYDC35oMiutO9ehTdLDs+1JC1RF/uL27xMe3hVD7Hdts8ZIqU94iY2v9RU9XqLz+1vlqUAr9dE2jcfl0IKh8cj1oeYoZWyHUZkZv+34xaHrehirS7kJJzwHUCrewYC25B8PQHIGOUwWaBg2/x+KhHWTEUmltckvXNHlyG7akelk6fL+pVJndmh+e2629zvoSVjNwtsnaE4Ix/18X51W+7h4F0BmjrhSkvcPj8TfvG/6ipNVHqrN0PLhIf+CPI9TROFQOVPqjE0R+hkVX5Lbi20wYbqxdTHZ11Tk48II5frzSrOr+5Srzu7XuVdGYOcNXGWh5ejTyJOd+q5NOmpJDffJALx/JIqaRlTTCEiL0nh8vpP9hBqRkxjJ9JhpeF/lqpBED2NnrhRftgy//L4vRfdwnJ5uRb4lg1KQez0EsV3iCgaK2xB6R1Jht4eaIxc9NQkTNACVbbUKRfSwPz2KRG8WWKPSlmi9kBI6k81hTny7QKm0BEPkO/MaxHNZrDHjcmx73FHI9cp9eUW729P9BzDY1jBJXpUY2OISwZqdn8DIaobZ4L4vRfdwnJ5vxVajijX/olKdyCoBE3J/ElpV3PVTePGUJZqibPruyG25E+r8ZfHYNPPHwJM91RHILUTWIXPBl70UbYt41AQeYbWhV8iPG82ot3+DeVtoOAMrKB+CSvojDFF7W/M2OwBUdxxJsGbzaMjzVtpJhJY+MHc5KPGPHBIx+rZKvCCIP1GjSMXSxHkjZ/rUniIGmxa5wPpPV0ZSMv9iAtSS5YBql5wn2Own5t811ZN9jCkxXPmc+eX+OysaOEdPlLkyDLMHCbhuhdJZ/iHWp+ZqIr5rDvKRlAKCHWoNwPpPV0ZSMvzeMUjYx7xIp83fkCy0HT+x5JWYrQYX/F2Qvc/aD4QI5TGEY5jKVDHmLWOdECPQd+q1m5xIViXecKELT8PPIMHTqUA1K/In41bj72Dc0ABO4ska/9lhJBIbI0DbA0PQPUkYGO654qVFcqx8NSjXTltLNn8hBxg9/+rcc+E+whLpIsDu0HhdTNgJzVadT6E80bdNomk5SuGcpTTQ59QBwg1G5qePpxSHeZQhF30C3lxeFGfvs5Ar0aC5+wFBpT/OWHYod8W1RBa+xqE2ke9YnGVJU03s1xF84Fe1u4fLr1IvPaH6NumZaAaR6LUcwY6jyIiAI/HQnx1Lh0BRUiwi7sqY3s5jdtOfO8Bxk7IwFHAmzAec53Oe3kVS9510wVGTGjhovpiPBzcR02v+O/9uH3A/s00G+tegYmd6e43SmfG0OEJrmCE/DXwJ32vGTOHYxg0FP6F9EkhlmXGhDvUpU3ztcmp8d3l/I1O3LPgQiChrVlaxMD3sFKEHiAjzCeLr/JKgoXy16eGlPDmAXrXEYZfU=",
            "items": [
                {
                    "cost": 100,
                    "description": "Widgets",
                    "line_total": 100,
                    "product_code": "9999-A",
                    "qty": 1,
                    "sku": "9999"
                }
            ],
            "recipients": [
                {
                    "address_1": "1 Fairfield Road",
                    "city": "Austin",
                    "country": "USA",
                    "email": "james@smith.com",
                    "first_name": "James",
                    "last_name": "Smith",
                    "phone_number": "555-555-55555",
                    "post_code": "55555-1234",
                    "state": "TX"
                }
            ],
            "shipping_address": {
                "address_1": "23 Smith Road",
                "city": "Canberra",
                "country": "AUS",
                "email": "{0}@email.com".format(shipping_type),
                "first_name": "James",
                "home_phone": "0421858999",
                "last_name": "Smith",
                "post_code": "2600",
                "shipping_method": "express",
            },
            "custom": {
                "3": "Facebook"
            },
            "website": "http://www.website.com"
        }
        return payload

    def test_successful_query(self):
        gw = fatzebra.gateway.Gateway()
        ref = "pytest-" + str(random.random())
        result = gw.purchase(
            100,
            ref,
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(result.successful)
        query = gw.query(result.id)
        self.assertTrue(result.successful)
        self.assertEqual(result.reference,ref)

    def test_failed_query(self):
        gw = fatzebra.gateway.Gateway()
        ref = "pytest-" + str(random.random())
        result = gw.purchase(
            151, # Amount ending in 51 etc will return error.
            ref,
            "Test Card",
            DECLINED_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertFalse(result.successful)
        query = gw.query(result.id)
        self.assertEqual(result.reference,ref)

    def test_purchase_with_invalid_card_responds_properly(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.purchase(
            151, # Amount ending in 51 etc will return error.
            "pytest-" + str(random.random()),
            "Test Card",
            DECLINED_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertFalse(result.successful)

    def test_errors_are_handled_properly(self):
        gw = fatzebra.gateway.Gateway()
        with self.assertRaises(fatzebra.errors.GatewayError):
            result = gw.purchase(
                100,
                "pytest-" + str(random.random()),
                "Test Card",
                INVALID_CARD,
                VALID_EXPIRY,
                "123",
                "1.2.3.4")

    def test_tokenize(self):
        gw = fatzebra.gateway.Gateway()
        result = gw.tokenize("Jim Murphy", VALID_CARD, VALID_EXPIRY, "123")
        self.assertIsNotNone(result.token)

    def test_token_purchase(self):
        gw = fatzebra.gateway.Gateway()
        card = gw.tokenize("Jim Murphy", VALID_CARD, VALID_EXPIRY, "123")
        result = gw.purchase_with_token(
            100, "pytoken" + str(random.random()), card.token, None, "1.2.3.4")
        self.assertTrue(result.successful)

    def test_invalid_token_purchase(self):
        gw = fatzebra.gateway.Gateway()
        with self.assertRaises(fatzebra.errors.GatewayUnknownResponseError):
            result = gw.purchase_with_token(
                100, "pytoken" + str(random.random()), "abc123", None,
                "1.2.3.4")

    def test_authentication_error(self):
        gw = fatzebra.gateway.Gateway("INVALID", "USER")
        with self.assertRaises(fatzebra.errors.AuthenticationError):
            gw.tokenize("Jim Smith", VALID_CARD, VALID_EXPIRY, "123")

    def test_refund(self):
        gw = fatzebra.gateway.Gateway()
        purchase = gw.purchase(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(purchase.successful)

        response = gw.refund(
            purchase.id,
            purchase.amount,
            "pyrefundtest" + str(random.random())
        )
        self.assertTrue(response.successful)

    def test_unmatched_refund(self):
        gw = fatzebra.gateway.Gateway()
        response = gw.unmatched_refund(
            100,
            "pytest-" + str(random.random()),
            "Test Card",
            VALID_CARD,
            VALID_EXPIRY,
            "123",
            "1.2.3.4")
        self.assertTrue(response.successful)

if __name__ == '__main__':
    unittest.main()
