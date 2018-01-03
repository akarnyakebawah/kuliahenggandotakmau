## Twiggsy Web


## Getting started
* Installation*
Install once globally:
```
  pip install -r requirements.txt
```
You will need Node >= 6 to run this project

* Run development server *
```
  python manage.py runserver
```


## API v1:

User

- List Create User
/v1/users/
fields:
    name: required,
    email: required,
    birth_date: required, YYYY-MM-DD
    password: write_only, required
    id: read_only,

- Retrieve Update Destroy User
/v1/users/(?P<user_id>\d+)/


Campaign

- List Create Campaign
/v1/campaigns/
fields:
    name: required,
    campaign_url: required, alhpanumeric
    twibbon_img: required, 1x1 ratio
    user
    created_at
    // fields below are not used (yet)
    started_at
    finished_at
    description
    caption_template
    header_img
    latitude
    longtitude
    city

- Retrieve Update Destroy Campaign
/v1/campaigns/(?P<campaign_url>[-\w]+)/


Twibbon

- List Create Twibbon
/v1/campaigns/(?P<campaign_url>[-\w]+)/twibbons/

fields:
    campaign: required,
    img: required,
    user
    caption
    created_at

- Retrieve Update Destroy Twibbon
/v1/campaigns/(?P<campaign_url>[-\w]+)/twibbons/(?P<twibbon_id>\d+)/


Helper

- List Create Temporary Image
/v1/helper/images/

fields:
    img: required
    relative_img
    created_at


Auth

- Obtain JWT Token
/v1/auth/

fields:
    email: required,
    password: required,
