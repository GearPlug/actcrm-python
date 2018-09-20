# actcrm-python
Act! CRM API wrapper written in python

# Batchbook-python
Batchbook API wrapper written in python.

## Installing
```
pip install actcrm-python
```

## Usage
### Simple access with API KEY
```
from actcrm.client import Client
client = Client('API_KEY', 'DEVELOPER_KEY')
```

Create a contact
```
client.create_contact()
```
Or you can specify what you want to send. Every field must be a string.
```
client.create_contact(firstName='Jhon', lastName='Snow', mobilePhone='0000000')
```

Get Contacts
```
client.get_contacts()
```
You can use OData query parameter to filter the contacts
```
client.get_contacts(top=1, order_by='created desc', filter='. . .')
```

Get an specific contact
```
client.get_contact(contact_id)
```

Delete an specific contact
```
client.delete_contact(contact_id)
```


You can do the same with opportunities
```
client.create_opportunity()
```


Get Metadata
```
client.get_metadata()
```

## Requirements

```
-Requests
-Urllib
```

## TODO
- Calendar
- Campaigns
- ContactActivities
- Emarketing
- Groups Show/Hide List Operations Expand Operations
- Interactions
- Todos
- UserInfos
