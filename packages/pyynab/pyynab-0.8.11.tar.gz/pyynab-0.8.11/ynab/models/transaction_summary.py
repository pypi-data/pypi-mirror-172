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


class TransactionSummary(object):
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
        'account_id': 'str',
        'amount': 'int',
        'approved': 'bool',
        'category_id': 'str',
        'cleared': 'str',
        'date': 'date',
        'deleted': 'bool',
        'flag_color': 'str',
        'id': 'str',
        'import_id': 'str',
        'matched_transaction_id': 'str',
        'memo': 'str',
        'payee_id': 'str',
        'transfer_account_id': 'str',
        'transfer_transaction_id': 'str'
    }

    attribute_map = {
        'account_id': 'account_id',
        'amount': 'amount',
        'approved': 'approved',
        'category_id': 'category_id',
        'cleared': 'cleared',
        'date': 'date',
        'deleted': 'deleted',
        'flag_color': 'flag_color',
        'id': 'id',
        'import_id': 'import_id',
        'matched_transaction_id': 'matched_transaction_id',
        'memo': 'memo',
        'payee_id': 'payee_id',
        'transfer_account_id': 'transfer_account_id',
        'transfer_transaction_id': 'transfer_transaction_id'
    }

    def __init__(self, account_id=None, amount=None, approved=None, category_id=None, cleared=None, date=None, deleted=None, flag_color=None, id=None, import_id=None, matched_transaction_id=None, memo=None, payee_id=None, transfer_account_id=None, transfer_transaction_id=None):  # noqa: E501
        """TransactionSummary - a model defined in OpenAPI"""  # noqa: E501

        self._account_id = None
        self._amount = None
        self._approved = None
        self._category_id = None
        self._cleared = None
        self._date = None
        self._deleted = None
        self._flag_color = None
        self._id = None
        self._import_id = None
        self._matched_transaction_id = None
        self._memo = None
        self._payee_id = None
        self._transfer_account_id = None
        self._transfer_transaction_id = None
        self.discriminator = None

        self.account_id = account_id
        self.amount = amount
        self.approved = approved
        self.category_id = category_id
        self.cleared = cleared
        self.date = date
        self.deleted = deleted
        self.flag_color = flag_color
        self.id = id
        self.import_id = import_id
        self.matched_transaction_id = matched_transaction_id
        self.memo = memo
        self.payee_id = payee_id
        self.transfer_account_id = transfer_account_id
        self.transfer_transaction_id = transfer_transaction_id

    @property
    def account_id(self):
        """Gets the account_id of this TransactionSummary.  # noqa: E501


        :return: The account_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this TransactionSummary.


        :param account_id: The account_id of this TransactionSummary.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def amount(self):
        """Gets the amount of this TransactionSummary.  # noqa: E501

        The transaction amount in milliunits format  # noqa: E501

        :return: The amount of this TransactionSummary.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this TransactionSummary.

        The transaction amount in milliunits format  # noqa: E501

        :param amount: The amount of this TransactionSummary.  # noqa: E501
        :type: int
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def approved(self):
        """Gets the approved of this TransactionSummary.  # noqa: E501

        Whether or not the transaction is approved  # noqa: E501

        :return: The approved of this TransactionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._approved

    @approved.setter
    def approved(self, approved):
        """Sets the approved of this TransactionSummary.

        Whether or not the transaction is approved  # noqa: E501

        :param approved: The approved of this TransactionSummary.  # noqa: E501
        :type: bool
        """
        if approved is None:
            raise ValueError("Invalid value for `approved`, must not be `None`")  # noqa: E501

        self._approved = approved

    @property
    def category_id(self):
        """Gets the category_id of this TransactionSummary.  # noqa: E501


        :return: The category_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this TransactionSummary.


        :param category_id: The category_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._category_id = category_id

    @property
    def cleared(self):
        """Gets the cleared of this TransactionSummary.  # noqa: E501

        The cleared status of the transaction  # noqa: E501

        :return: The cleared of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._cleared

    @cleared.setter
    def cleared(self, cleared):
        """Sets the cleared of this TransactionSummary.

        The cleared status of the transaction  # noqa: E501

        :param cleared: The cleared of this TransactionSummary.  # noqa: E501
        :type: str
        """
        if cleared is None:
            raise ValueError("Invalid value for `cleared`, must not be `None`")  # noqa: E501
        allowed_values = ["cleared", "uncleared", "reconciled"]  # noqa: E501
        if cleared not in allowed_values:
            raise ValueError(
                "Invalid value for `cleared` ({0}), must be one of {1}"  # noqa: E501
                .format(cleared, allowed_values)
            )

        self._cleared = cleared

    @property
    def date(self):
        """Gets the date of this TransactionSummary.  # noqa: E501

        The transaction date in ISO format (e.g. 2016-12-01)  # noqa: E501

        :return: The date of this TransactionSummary.  # noqa: E501
        :rtype: date
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this TransactionSummary.

        The transaction date in ISO format (e.g. 2016-12-01)  # noqa: E501

        :param date: The date of this TransactionSummary.  # noqa: E501
        :type: date
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def deleted(self):
        """Gets the deleted of this TransactionSummary.  # noqa: E501

        Whether or not the transaction has been deleted.  Deleted transactions will only be included in delta requests.  # noqa: E501

        :return: The deleted of this TransactionSummary.  # noqa: E501
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this TransactionSummary.

        Whether or not the transaction has been deleted.  Deleted transactions will only be included in delta requests.  # noqa: E501

        :param deleted: The deleted of this TransactionSummary.  # noqa: E501
        :type: bool
        """
        if deleted is None:
            raise ValueError("Invalid value for `deleted`, must not be `None`")  # noqa: E501

        self._deleted = deleted

    @property
    def flag_color(self):
        """Gets the flag_color of this TransactionSummary.  # noqa: E501

        The transaction flag  # noqa: E501

        :return: The flag_color of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._flag_color

    @flag_color.setter
    def flag_color(self, flag_color):
        """Sets the flag_color of this TransactionSummary.

        The transaction flag  # noqa: E501

        :param flag_color: The flag_color of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._flag_color = flag_color

    @property
    def id(self):
        """Gets the id of this TransactionSummary.  # noqa: E501


        :return: The id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TransactionSummary.


        :param id: The id of this TransactionSummary.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def import_id(self):
        """Gets the import_id of this TransactionSummary.  # noqa: E501

        If the Transaction was imported, this field is a unique (by account) import identifier.  If this transaction was imported through File Based Import or Direct Import and not through the API, the import_id will have the format: 'YNAB:[milliunit_amount]:[iso_date]:[occurrence]'.  For example, a transaction dated 2015-12-30 in the amount of -$294.23 USD would have an import_id of 'YNAB:-294230:2015-12-30:1'.  If a second transaction on the same account was imported and had the same date and same amount, its import_id would be 'YNAB:-294230:2015-12-30:2'.  # noqa: E501

        :return: The import_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._import_id

    @import_id.setter
    def import_id(self, import_id):
        """Sets the import_id of this TransactionSummary.

        If the Transaction was imported, this field is a unique (by account) import identifier.  If this transaction was imported through File Based Import or Direct Import and not through the API, the import_id will have the format: 'YNAB:[milliunit_amount]:[iso_date]:[occurrence]'.  For example, a transaction dated 2015-12-30 in the amount of -$294.23 USD would have an import_id of 'YNAB:-294230:2015-12-30:1'.  If a second transaction on the same account was imported and had the same date and same amount, its import_id would be 'YNAB:-294230:2015-12-30:2'.  # noqa: E501

        :param import_id: The import_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._import_id = import_id

    @property
    def matched_transaction_id(self):
        """Gets the matched_transaction_id of this TransactionSummary.  # noqa: E501

        If transaction is matched, the id of the matched transaction  # noqa: E501

        :return: The matched_transaction_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._matched_transaction_id

    @matched_transaction_id.setter
    def matched_transaction_id(self, matched_transaction_id):
        """Sets the matched_transaction_id of this TransactionSummary.

        If transaction is matched, the id of the matched transaction  # noqa: E501

        :param matched_transaction_id: The matched_transaction_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._matched_transaction_id = matched_transaction_id

    @property
    def memo(self):
        """Gets the memo of this TransactionSummary.  # noqa: E501


        :return: The memo of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this TransactionSummary.


        :param memo: The memo of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def payee_id(self):
        """Gets the payee_id of this TransactionSummary.  # noqa: E501


        :return: The payee_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._payee_id

    @payee_id.setter
    def payee_id(self, payee_id):
        """Sets the payee_id of this TransactionSummary.


        :param payee_id: The payee_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._payee_id = payee_id

    @property
    def transfer_account_id(self):
        """Gets the transfer_account_id of this TransactionSummary.  # noqa: E501

        If a transfer transaction, the account to which it transfers  # noqa: E501

        :return: The transfer_account_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._transfer_account_id

    @transfer_account_id.setter
    def transfer_account_id(self, transfer_account_id):
        """Sets the transfer_account_id of this TransactionSummary.

        If a transfer transaction, the account to which it transfers  # noqa: E501

        :param transfer_account_id: The transfer_account_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._transfer_account_id = transfer_account_id

    @property
    def transfer_transaction_id(self):
        """Gets the transfer_transaction_id of this TransactionSummary.  # noqa: E501

        If a transfer transaction, the id of transaction on the other side of the transfer  # noqa: E501

        :return: The transfer_transaction_id of this TransactionSummary.  # noqa: E501
        :rtype: str
        """
        return self._transfer_transaction_id

    @transfer_transaction_id.setter
    def transfer_transaction_id(self, transfer_transaction_id):
        """Sets the transfer_transaction_id of this TransactionSummary.

        If a transfer transaction, the id of transaction on the other side of the transfer  # noqa: E501

        :param transfer_transaction_id: The transfer_transaction_id of this TransactionSummary.  # noqa: E501
        :type: str
        """

        self._transfer_transaction_id = transfer_transaction_id

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
        if not isinstance(other, TransactionSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
