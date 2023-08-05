# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import ynab
from ynab.models.save_sub_transaction import SaveSubTransaction  # noqa: E501
from ynab.rest import ApiException


class TestSaveSubTransaction(unittest.TestCase):
    """SaveSubTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSaveSubTransaction(self):
        """Test SaveSubTransaction"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ynab.models.save_sub_transaction.SaveSubTransaction()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
