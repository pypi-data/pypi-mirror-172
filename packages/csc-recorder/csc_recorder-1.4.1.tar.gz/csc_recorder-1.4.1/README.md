# csc-recorder

Python wrapper for CSC Recorder.

`pip install csc-recorder`


## Usuage

```
from csc_recorder.CSCRecorder import CSCRecorder


client = CSCRecorder('host', 'username', 'password')

# Sending a package
data, response = client.send_package('1234_TEST', '48201', 'Default Office', {'document_name': 'test', 'document_type': 'Deed'}, 'paperfulfillment', True)

```
The first three params are required:
- client_package_id
- fips
- assigned_office

The dictionary in the params supports the below attributes, they're not required:
- document_name
- document_type
- send_to_county
- send_to_state
- grantee_first_name
- grantee_last_name
- grantee_middle_name
- grantee_suffix
- grantee_title
- grantor_first_name
- grantor_first_name
- grantor_last_name
- grantor_middle_name
- grantor_suffix
- grantor_title
- consideration_amount
- original_recording_date
- original_instrument_no
- original_deed_book
- original_deed_page
- assesors_parcel_id
- date_of_note
- amount_of_note
- property_street_address_1
- property_city
- property_state
- property_zip
- requesting_name
- return_name
- return_company
- return_street_address_1
- return_city
- return_state
- return_zip
- requesting_company
- requesting_address_1
- requesting_city
- requesting_state
- requesting_zip
- doc_image **(NOTE: base64 PDF's)

The last 2 params are optional as well.
- service_type, defaults to None, but currently you can also add 'paperfulillment'
- no_document, defaults to False, but you can make the package send 0 document attributes by marking True