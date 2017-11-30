# coding: utf-8

"""
    TheTVDB API v2

    API v2 targets v1 functionality with a few minor additions. The API is accessible via https://api.thetvdb.com and provides the following REST endpoints in JSON format.   How to use this API documentation ----------------   You may browse the API routes without authentication, but if you wish to send requests to the API and see response data, then you must authenticate. 1. Obtain a JWT token by `POST`ing  to the `/login` route in the `Authentication` section with your API key and credentials. 1. Paste the JWT token from the response into the \"JWT Token\" field at the top of the page and click the 'Add Token' button.   You will now be able to use the remaining routes to send requests to the API and get a response.   Language Selection ----------------   Language selection is done via the `Accept-Language` header. At the moment, you may only pass one language abbreviation in the header at a time. Valid language abbreviations can be found at the `/languages` route..   Authentication ----------------   Authentication to use the API is similar to the How-to section above. Users must `POST` to the `/login` route with their API key and credentials in the following format in order to obtain a JWT token.  `{\"apikey\":\"APIKEY\",\"username\":\"USERNAME\",\"userkey\":\"USERKEY\"}`  Note that the username and key are ONLY required for the `/user` routes. The user's key is labled `Account Identifier` in the account section of the main site. The token is then used in all subsequent requests by providing it in the `Authorization` header. The header will look like: `Authorization: Bearer <yourJWTtoken>`. Currently, the token expires after 24 hours. You can `GET` the `/refresh_token` route to extend that expiration date.   Versioning ----------------   You may request a different version of the API by including an `Accept` header in your request with the following format: `Accept:application/vnd.thetvdb.v$VERSION`. This documentation automatically uses the version seen at the top and bottom of the page.

    OpenAPI spec version: 2.1.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SeriesImageQueryResult(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'file_name': 'str',
        'id': 'int',
        'key_type': 'str',
        'language_id': 'int',
        'ratings_info': 'SeriesImageQueryResultRatingsInfo',
        'resolution': 'str',
        'sub_key': 'str',
        'thumbnail': 'str'
    }

    attribute_map = {
        'file_name': 'fileName',
        'id': 'id',
        'key_type': 'keyType',
        'language_id': 'languageId',
        'ratings_info': 'ratingsInfo',
        'resolution': 'resolution',
        'sub_key': 'subKey',
        'thumbnail': 'thumbnail'
    }

    def __init__(self, file_name=None, id=None, key_type=None, language_id=None, ratings_info=None, resolution=None, sub_key=None, thumbnail=None):
        """
        SeriesImageQueryResult - a model defined in Swagger
        """

        self._file_name = None
        self._id = None
        self._key_type = None
        self._language_id = None
        self._ratings_info = None
        self._resolution = None
        self._sub_key = None
        self._thumbnail = None

        if file_name is not None:
          self.file_name = file_name
        if id is not None:
          self.id = id
        if key_type is not None:
          self.key_type = key_type
        if language_id is not None:
          self.language_id = language_id
        if ratings_info is not None:
          self.ratings_info = ratings_info
        if resolution is not None:
          self.resolution = resolution
        if sub_key is not None:
          self.sub_key = sub_key
        if thumbnail is not None:
          self.thumbnail = thumbnail

    @property
    def file_name(self):
        """
        Gets the file_name of this SeriesImageQueryResult.

        :return: The file_name of this SeriesImageQueryResult.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """
        Sets the file_name of this SeriesImageQueryResult.

        :param file_name: The file_name of this SeriesImageQueryResult.
        :type: str
        """

        self._file_name = file_name

    @property
    def id(self):
        """
        Gets the id of this SeriesImageQueryResult.

        :return: The id of this SeriesImageQueryResult.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SeriesImageQueryResult.

        :param id: The id of this SeriesImageQueryResult.
        :type: int
        """

        self._id = id

    @property
    def key_type(self):
        """
        Gets the key_type of this SeriesImageQueryResult.

        :return: The key_type of this SeriesImageQueryResult.
        :rtype: str
        """
        return self._key_type

    @key_type.setter
    def key_type(self, key_type):
        """
        Sets the key_type of this SeriesImageQueryResult.

        :param key_type: The key_type of this SeriesImageQueryResult.
        :type: str
        """

        self._key_type = key_type

    @property
    def language_id(self):
        """
        Gets the language_id of this SeriesImageQueryResult.

        :return: The language_id of this SeriesImageQueryResult.
        :rtype: int
        """
        return self._language_id

    @language_id.setter
    def language_id(self, language_id):
        """
        Sets the language_id of this SeriesImageQueryResult.

        :param language_id: The language_id of this SeriesImageQueryResult.
        :type: int
        """

        self._language_id = language_id

    @property
    def ratings_info(self):
        """
        Gets the ratings_info of this SeriesImageQueryResult.

        :return: The ratings_info of this SeriesImageQueryResult.
        :rtype: SeriesImageQueryResultRatingsInfo
        """
        return self._ratings_info

    @ratings_info.setter
    def ratings_info(self, ratings_info):
        """
        Sets the ratings_info of this SeriesImageQueryResult.

        :param ratings_info: The ratings_info of this SeriesImageQueryResult.
        :type: SeriesImageQueryResultRatingsInfo
        """

        self._ratings_info = ratings_info

    @property
    def resolution(self):
        """
        Gets the resolution of this SeriesImageQueryResult.

        :return: The resolution of this SeriesImageQueryResult.
        :rtype: str
        """
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """
        Sets the resolution of this SeriesImageQueryResult.

        :param resolution: The resolution of this SeriesImageQueryResult.
        :type: str
        """

        self._resolution = resolution

    @property
    def sub_key(self):
        """
        Gets the sub_key of this SeriesImageQueryResult.

        :return: The sub_key of this SeriesImageQueryResult.
        :rtype: str
        """
        return self._sub_key

    @sub_key.setter
    def sub_key(self, sub_key):
        """
        Sets the sub_key of this SeriesImageQueryResult.

        :param sub_key: The sub_key of this SeriesImageQueryResult.
        :type: str
        """

        self._sub_key = sub_key

    @property
    def thumbnail(self):
        """
        Gets the thumbnail of this SeriesImageQueryResult.

        :return: The thumbnail of this SeriesImageQueryResult.
        :rtype: str
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        """
        Sets the thumbnail of this SeriesImageQueryResult.

        :param thumbnail: The thumbnail of this SeriesImageQueryResult.
        :type: str
        """

        self._thumbnail = thumbnail

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, SeriesImageQueryResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
