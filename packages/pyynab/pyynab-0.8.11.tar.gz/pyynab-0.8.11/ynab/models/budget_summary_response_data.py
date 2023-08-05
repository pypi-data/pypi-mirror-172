# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class BudgetSummaryResponseData(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'budgets': 'list[BudgetSummary]',
        'default_budget': 'BudgetSummary'
    }

    attribute_map = {
        'budgets': 'budgets',
        'default_budget': 'default_budget'
    }

    def __init__(self, budgets=None, default_budget=None):  # noqa: E501
        """BudgetSummaryResponseData - a model defined in OpenAPI"""  # noqa: E501

        self._budgets = None
        self._default_budget = None
        self.discriminator = None

        self.budgets = budgets
        if default_budget is not None:
            self.default_budget = default_budget

    @property
    def budgets(self):
        """Gets the budgets of this BudgetSummaryResponseData.  # noqa: E501


        :return: The budgets of this BudgetSummaryResponseData.  # noqa: E501
        :rtype: list[BudgetSummary]
        """
        return self._budgets

    @budgets.setter
    def budgets(self, budgets):
        """Sets the budgets of this BudgetSummaryResponseData.


        :param budgets: The budgets of this BudgetSummaryResponseData.  # noqa: E501
        :type: list[BudgetSummary]
        """
        if budgets is None:
            raise ValueError("Invalid value for `budgets`, must not be `None`")  # noqa: E501

        self._budgets = budgets

    @property
    def default_budget(self):
        """Gets the default_budget of this BudgetSummaryResponseData.  # noqa: E501


        :return: The default_budget of this BudgetSummaryResponseData.  # noqa: E501
        :rtype: BudgetSummary
        """
        return self._default_budget

    @default_budget.setter
    def default_budget(self, default_budget):
        """Sets the default_budget of this BudgetSummaryResponseData.


        :param default_budget: The default_budget of this BudgetSummaryResponseData.  # noqa: E501
        :type: BudgetSummary
        """

        self._default_budget = default_budget

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BudgetSummaryResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
