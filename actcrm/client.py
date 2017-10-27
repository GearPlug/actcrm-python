from requests.auth import HTTPBasicAuth
import json
import requests

BASE_URL = "https://mycloud.act.com/act/api"


class Client(object):
    auth = None

    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username=username, password=password)

    def _get(self, endpoint, data=None, **kwargs):
        return self._request('GET', endpoint, data=data, **kwargs)

    def _delete(self, endpoint, data=None, **kwargs):
        return self._request('DELETE', endpoint, data=data, **kwargs)

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
        if response.status_code == 204:
            return True
        elif response.status_code == 400:
            raise Exception("The URL {0} retrieved an {1} error. Please check your request body and try again.\nRaw "
                            "message: {2}".format(response.url, response.status_code, response.text))
        elif response.status_code == 401:
            raise Exception("The URL {0} retrieved and {1} error. Please check your credentials, "
                            "make sure you have permission to perform this action andtry again.".format(
                response.url, response.status_code))
        elif response.status_code == 404:
            raise Exception("The URL {0} retrieved an {1} error. Please check the URL and try again.\nRaw message: {"
                            "2}".format(response.url, response.status_code, response.text))
        return response.json()

    def get_contacts(self, **kwargs):
        return self._get('Contacts', **kwargs)

    def get_contact(self, id):
        return self._get('Contacts/{0}'.format(id))

    def create_contact(self, firstName='Default Name', **kwargs):
        """
          Aditional data:
            lastName, company, jobTitle, emailAddress, altEmailAddress,
             businessPhone, mobilePhone, homePhone, website, linkedinUrl, birthday
        :return:
        """
        kwargs.update({'firstName': firstName})
        return self._post('Contacts', data=kwargs, headers={'Content-Type': 'application/json'})

    def get_opportunities(self, **kwargs):
        return self._get('Opportunities', **kwargs)

    def get_opportunity(self, id):
        return self._get('Opportunities/{}'.format(id))

    def get_opportunity_stages(self):
        return self._get('OpportunityStages')

    def create_opportunity(self, title='Default Title', stage='Leads', **kwargs):
        """
        title, stage,* description, total, currency, notes, estimatedClose, estimatedClose,actualClose, customField1

        contacts??
        :return:
        """
        kwargs.update({'title': title, 'stage': stage})
        return self._post('Opportunities', data=kwargs, headers={'Content-Type': 'application/json'})

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

    def delete_contact(self, id):
        return self._delete('Contacts/{0}'.format(id))

    def delete_opportunity(self, id):
        return self._delete('Opportunities/{0}'.format(id))

    def get_webhooks(self):
        return self._get('Webhooks')

    def create_webhook(self, url, event):
        return self._post('Webhooks', data={'target_url': url, 'event': event},
                          headers={'Content-Type': 'application/json'})

    def delete_webhook(self, id):
        """
        No se como obtener el id del webhook. Otra forma de borrarlo es devolviendo status 410 (gone) en el response.
        :param id:
        :return:
        """
        return self._delete('Webhooks/{0}'.format(id))
