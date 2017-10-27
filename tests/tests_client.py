import os
from unittest import TestCase
from actcrm.client import Client


class TypeformTestCases(TestCase):
    """
        You must set your API_KEY (given by the user) and your DEVELOPER_KEY in the environmental variables.
    """
    contact = {'firstName': 'TestContactLib', 'lastName': 'Python', 'mobilePhone': '000111000', 'id': None}
    opportunity = {'title': 'TestOportunityLib', 'description': 'This is a test opportunity created to run unittest',
                   'stage': 'Leads', 'id': None}

    def setUp(self):
        self.url_webhook = os.environ.get('webhook_url')
        self.client = Client(os.environ.get('API_KEY'), os.environ.get('DEVELOPER_KEY'))

    def test_contact(self):
        # Create contact
        response = self.client.create_contact(**self.contact)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['firstName'], self.contact['firstName'])
        self.assertEqual(response['lastName'], self.contact['lastName'])
        self.assertEqual(response['mobilePhone'], self.contact['mobilePhone'])
        self.assertIn('created', response)
        self.assertIn('id', response)
        self.contact['id'] = response['id']

        # Get multiple contacts, use top to limit the list
        response = self.client.get_contacts(top=5)
        self.assertTrue(len(response) <= 5)

        # Get last contact
        response = self.client.get_contacts(order_by='created desc', top=1)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)

        # Check the last contact is the same we created
        self.assertEqual(self.contact['id'], response[0]['id'])

        # Get single contact
        response = self.client.get_contact(self.contact['id'])
        self.assertIsInstance(response, dict)
        self.assertEqual(response['id'], self.contact['id'])

        # Delete contact
        response = self.client.delete_contact(self.contact['id'])
        self.assertTrue(response)

    def test_opportunity(self):
        # Create opportunity
        response = self.client.create_opportunity(**self.opportunity)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['title'], self.opportunity['title'])
        self.assertEqual(response['description'], self.opportunity['description'])
        self.assertEqual(response['stage'], self.opportunity['stage'])
        self.assertIn('created', response)
        self.assertIn('id', response)
        self.opportunity['id'] = response['id']

        # Get multiple opportunities, use top to limit the list
        response = self.client.get_opportunities(top=5)
        self.assertTrue(len(response) <= 5)

        # Get last contact
        response = self.client.get_opportunities(order_by='created desc', top=1)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)

        # Check the last contact is the same we created
        self.assertEqual(self.opportunity['id'], response[0]['id'])

        # Get single contact
        response = self.client.get_opportunity(self.opportunity['id'])
        self.assertIsInstance(response, dict)
        self.assertEqual(response['id'], self.opportunity['id'])

        # Delete contact
        response = self.client.delete_opportunity(self.opportunity['id'])
        self.assertTrue(response)


