import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint

API_KEY = "1vS-WEV1xhc27unvN60dcpGg0Tsjb00uF5XFpnN59Cs"
DEVELOPER_KEY = "62228d9fcd9ae7b8b3b0f74d12cbb583"
BASE_URL = "https://mycloud.act.com/act/api/"


# $top = MAX_LIMIT
# $filter = VAR eq 'String'
# $orderby = 'created'  (optional) desc
# $select = field list


class Client(object):
    auth = None

    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username=username, password=password)

    def _get(self, endpoint, data=None, **kwargs):
        return self._request('GET', endpoint, data=data, **kwargs)

    def _post(self, endpoint, data=None, **kwargs):
        return self._request('POST', endpoint, data=data, **kwargs)

    def _request(self, method, endpoint, data=None, top=None, filter=None, order_by=None, select=None,
                 headers={}, **kwargs):
        extra = {}
        if top is not None and isinstance(top, int):
            extra['$top'] = str(top)
        if order_by is not None and isinstance(order_by, str):
            extra['$orderby'] = order_by
        if filter is not None and isinstance(filter, str):
            extra['$filter'] = filter
        extra = '&'.join(['{0}={1}'.format(k, v) for k, v in extra.items()])
        url = '{0}/{1}?{2}'.format(BASE_URL, endpoint, extra)
        response = requests.request(method, url, auth=self.auth, data=json.dumps(data), headers=headers)
        return self._parse(response)

    def _parse(self, response):
        if response.status_code == 400:
            raise Exception("The URL {0} retrieved an {1} error. Please check your request body and try again.\nRaw "
                            "message: {2}".format(response.url, response.status_code, response.text))
        if response.status_code == 401:
            raise Exception("The URL {0} retrieved and {1} error. Please check your credentials, "
                            "make sure you have permission to perform this action andtry again.".format(
                response.url, response.status_code))
        elif response.status_code == 404:
            raise Exception("The URL {0} retrieved an {1} error. Please check the URL and try again.\nRaw message: {"
                            "2}".format(response.url, response.status_code, response.text))
        print("RESPONSE: \n", response.status_code)
        pprint(response.json())

        return response.json()

    def get_contacts(self, **kwargs):
        return self._get('Contacts', **kwargs)

    def get_contact(self, id):
        return self._get('Contacts/{}'.format(id))

    def get_oportunities(self, **kwargs):
        return self._get('Opportunities', **kwargs)

    def get_oportunity(self, id):
        return self._get('Opportunities/{}'.format(id))

    def get_metadata(self, type=None, only_visible=False):
        """
            Use to get custom fields

        :param type: Use 'Field' for Contacts custom fields and 'OpportunityField' for Opportunities custom fields.
        :return:
        """
        kwargs = {}
        if type is not None and type in ['Field', 'OpportunityField']:
            kwargs['filter'] = "type eq '{0}'".format(type)
        if only_visible is True:
            query_prefix = '' if '$filter' not in kwargs.keys() else '{0} and '.format(kwargs['filter'])
            kwargs['filter'] = query_prefix + 'show eq true'
        return self._get('Metadata', **kwargs)

    def create_contact(self, **kwargs):
        """
          firstName,* lastName, company, jobTitle, emailAddress, altEmailAddress, businessPhone, mobilePhone, homePhone,
          website, linkedinUrl, birthday
        :return:
        """
        return self._post('Contacts', data=kwargs, headers={'Content-Type': 'application/json'})

    def create_opportunity(self, **kwargs):
        """
        title, stage,* description, total, currency, notes, estimatedClose, estimatedClose,actualClose, customField1

        contacts??
        :return:
        """
        return self._post('Opportunities', data=kwargs, headers={'Content-Type': 'application/json'})


c = Client(API_KEY, DEVELOPER_KEY)
# c.get_contacts(top=1, order_by='created desc')
# c.get_contact("59f0c4aba5028e06703de9df")
# c.get_oportunities()
# c.get_oportunity('59f0c3604cee7a0bf4d0eeae')
# c.get_metadata(only_visible=True)
# c.create_contact(firstName="mAICOL", lastName="Carloss")
c.create_opportunity(title="El oportuno express", stage="Leads")
