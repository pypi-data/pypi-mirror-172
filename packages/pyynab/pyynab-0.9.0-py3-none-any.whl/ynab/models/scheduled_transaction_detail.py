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


class ScheduledTransactionDetail(object):
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
        'category_id': 'str',
        'date_first': 'date',
        'date_next': 'date',
        'deleted': 'bool',
        'flag_color': 'str',
        'frequency': 'str',
        'id': 'str',
        'memo': 'str',
        'payee_id': 'str',
        'transfer_account_id': 'str',
        'account_name': 'str',
        'category_name': 'str',
        'payee_name': 'str',
        'subtransactions': 'list[ScheduledSubTransaction]'
    }

    attribute_map = {
        'account_id': 'account_id',
        'amount': 'amount',
        'category_id': 'category_id',
        'date_first': 'date_first',
        'date_next': 'date_next',
        'deleted': 'deleted',
        'flag_color': 'flag_color',
        'frequency': 'frequency',
        'id': 'id',
        'memo': 'memo',
        'payee_id': 'payee_id',
        'transfer_account_id': 'transfer_account_id',
        'account_name': 'account_name',
        'category_name': 'category_name',
        'payee_name': 'payee_name',
        'subtransactions': 'subtransactions'
    }

    def __init__(self, account_id=None, amount=None, category_id=None, date_first=None, date_next=None, deleted=None, flag_color=None, frequency=None, id=None, memo=None, payee_id=None, transfer_account_id=None, account_name=None, category_name=None, payee_name=None, subtransactions=None):  # noqa: E501
        """ScheduledTransactionDetail - a model defined in OpenAPI"""  # noqa: E501

        self._account_id = None
        self._amount = None
        self._category_id = None
        self._date_first = None
        self._date_next = None
        self._deleted = None
        self._flag_color = None
        self._frequency = None
        self._id = None
        self._memo = None
        self._payee_id = None
        self._transfer_account_id = None
        self._account_name = None
        self._category_name = None
        self._payee_name = None
        self._subtransactions = None
        self.discriminator = None

        self.account_id = account_id
        self.amount = amount
        if category_id is not None:
            self.category_id = category_id
        self.date_first = date_first
        self.date_next = date_next
        self.deleted = deleted
        if flag_color is not None:
            self.flag_color = flag_color
        self.frequency = frequency
        self.id = id
        if memo is not None:
            self.memo = memo
        if payee_id is not None:
            self.payee_id = payee_id
        if transfer_account_id is not None:
            self.transfer_account_id = transfer_account_id
        self.account_name = account_name
        if category_name is not None:
            self.category_name = category_name
        if payee_name is not None:
            self.payee_name = payee_name
        self.subtransactions = subtransactions

    @property
    def account_id(self):
        """Gets the account_id of this ScheduledTransactionDetail.  # noqa: E501


        :return: The account_id of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this ScheduledTransactionDetail.


        :param account_id: The account_id of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def amount(self):
        """Gets the amount of this ScheduledTransactionDetail.  # noqa: E501

        The scheduled transaction amount in milliunits format  # noqa: E501

        :return: The amount of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this ScheduledTransactionDetail.

        The scheduled transaction amount in milliunits format  # noqa: E501

        :param amount: The amount of this ScheduledTransactionDetail.  # noqa: E501
        :type: int
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def category_id(self):
        """Gets the category_id of this ScheduledTransactionDetail.  # noqa: E501


        :return: The category_id of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this ScheduledTransactionDetail.


        :param category_id: The category_id of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._category_id = category_id

    @property
    def date_first(self):
        """Gets the date_first of this ScheduledTransactionDetail.  # noqa: E501

        The first date for which the Scheduled Transaction was scheduled.  # noqa: E501

        :return: The date_first of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: date
        """
        return self._date_first

    @date_first.setter
    def date_first(self, date_first):
        """Sets the date_first of this ScheduledTransactionDetail.

        The first date for which the Scheduled Transaction was scheduled.  # noqa: E501

        :param date_first: The date_first of this ScheduledTransactionDetail.  # noqa: E501
        :type: date
        """
        if date_first is None:
            raise ValueError("Invalid value for `date_first`, must not be `None`")  # noqa: E501

        self._date_first = date_first

    @property
    def date_next(self):
        """Gets the date_next of this ScheduledTransactionDetail.  # noqa: E501

        The next date for which the Scheduled Transaction is scheduled.  # noqa: E501

        :return: The date_next of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: date
        """
        return self._date_next

    @date_next.setter
    def date_next(self, date_next):
        """Sets the date_next of this ScheduledTransactionDetail.

        The next date for which the Scheduled Transaction is scheduled.  # noqa: E501

        :param date_next: The date_next of this ScheduledTransactionDetail.  # noqa: E501
        :type: date
        """
        if date_next is None:
            raise ValueError("Invalid value for `date_next`, must not be `None`")  # noqa: E501

        self._date_next = date_next

    @property
    def deleted(self):
        """Gets the deleted of this ScheduledTransactionDetail.  # noqa: E501

        Whether or not the scheduled transaction has been deleted.  Deleted scheduled transactions will only be included in delta requests.  # noqa: E501

        :return: The deleted of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this ScheduledTransactionDetail.

        Whether or not the scheduled transaction has been deleted.  Deleted scheduled transactions will only be included in delta requests.  # noqa: E501

        :param deleted: The deleted of this ScheduledTransactionDetail.  # noqa: E501
        :type: bool
        """
        if deleted is None:
            raise ValueError("Invalid value for `deleted`, must not be `None`")  # noqa: E501

        self._deleted = deleted

    @property
    def flag_color(self):
        """Gets the flag_color of this ScheduledTransactionDetail.  # noqa: E501

        The scheduled transaction flag  # noqa: E501

        :return: The flag_color of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._flag_color

    @flag_color.setter
    def flag_color(self, flag_color):
        """Sets the flag_color of this ScheduledTransactionDetail.

        The scheduled transaction flag  # noqa: E501

        :param flag_color: The flag_color of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """
        allowed_values = ["red", "orange", "yellow", "green", "blue", "purple"]  # noqa: E501
        if flag_color not in allowed_values:
            raise ValueError(
                "Invalid value for `flag_color` ({0}), must be one of {1}"  # noqa: E501
                .format(flag_color, allowed_values)
            )

        self._flag_color = flag_color

    @property
    def frequency(self):
        """Gets the frequency of this ScheduledTransactionDetail.  # noqa: E501


        :return: The frequency of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        """Sets the frequency of this ScheduledTransactionDetail.


        :param frequency: The frequency of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """
        if frequency is None:
            raise ValueError("Invalid value for `frequency`, must not be `None`")  # noqa: E501
        allowed_values = ["never", "daily", "weekly", "everyOtherWeek", "twiceAMonth", "every4Weeks", "monthly", "everyOtherMonth", "every3Months", "every4Months", "twiceAYear", "yearly", "everyOtherYear"]  # noqa: E501
        if frequency not in allowed_values:
            raise ValueError(
                "Invalid value for `frequency` ({0}), must be one of {1}"  # noqa: E501
                .format(frequency, allowed_values)
            )

        self._frequency = frequency

    @property
    def id(self):
        """Gets the id of this ScheduledTransactionDetail.  # noqa: E501


        :return: The id of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ScheduledTransactionDetail.


        :param id: The id of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def memo(self):
        """Gets the memo of this ScheduledTransactionDetail.  # noqa: E501


        :return: The memo of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this ScheduledTransactionDetail.


        :param memo: The memo of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def payee_id(self):
        """Gets the payee_id of this ScheduledTransactionDetail.  # noqa: E501


        :return: The payee_id of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._payee_id

    @payee_id.setter
    def payee_id(self, payee_id):
        """Sets the payee_id of this ScheduledTransactionDetail.


        :param payee_id: The payee_id of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._payee_id = payee_id

    @property
    def transfer_account_id(self):
        """Gets the transfer_account_id of this ScheduledTransactionDetail.  # noqa: E501

        If a transfer, the account_id which the scheduled transaction transfers to  # noqa: E501

        :return: The transfer_account_id of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._transfer_account_id

    @transfer_account_id.setter
    def transfer_account_id(self, transfer_account_id):
        """Sets the transfer_account_id of this ScheduledTransactionDetail.

        If a transfer, the account_id which the scheduled transaction transfers to  # noqa: E501

        :param transfer_account_id: The transfer_account_id of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._transfer_account_id = transfer_account_id

    @property
    def account_name(self):
        """Gets the account_name of this ScheduledTransactionDetail.  # noqa: E501


        :return: The account_name of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this ScheduledTransactionDetail.


        :param account_name: The account_name of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """
        if account_name is None:
            raise ValueError("Invalid value for `account_name`, must not be `None`")  # noqa: E501

        self._account_name = account_name

    @property
    def category_name(self):
        """Gets the category_name of this ScheduledTransactionDetail.  # noqa: E501


        :return: The category_name of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """Sets the category_name of this ScheduledTransactionDetail.


        :param category_name: The category_name of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._category_name = category_name

    @property
    def payee_name(self):
        """Gets the payee_name of this ScheduledTransactionDetail.  # noqa: E501


        :return: The payee_name of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._payee_name

    @payee_name.setter
    def payee_name(self, payee_name):
        """Sets the payee_name of this ScheduledTransactionDetail.


        :param payee_name: The payee_name of this ScheduledTransactionDetail.  # noqa: E501
        :type: str
        """

        self._payee_name = payee_name

    @property
    def subtransactions(self):
        """Gets the subtransactions of this ScheduledTransactionDetail.  # noqa: E501

        If a split scheduled transaction, the subtransactions.  # noqa: E501

        :return: The subtransactions of this ScheduledTransactionDetail.  # noqa: E501
        :rtype: list[ScheduledSubTransaction]
        """
        return self._subtransactions

    @subtransactions.setter
    def subtransactions(self, subtransactions):
        """Sets the subtransactions of this ScheduledTransactionDetail.

        If a split scheduled transaction, the subtransactions.  # noqa: E501

        :param subtransactions: The subtransactions of this ScheduledTransactionDetail.  # noqa: E501
        :type: list[ScheduledSubTransaction]
        """
        if subtransactions is None:
            raise ValueError("Invalid value for `subtransactions`, must not be `None`")  # noqa: E501

        self._subtransactions = subtransactions

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
        if not isinstance(other, ScheduledTransactionDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
