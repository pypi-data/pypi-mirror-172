Yelp Fusion API v3 Python Client
================================

.. meta::

   :description: yelpfusion3 is a Python 3 client library for Yelp Fusion API v3.
   :keywords: yelp, fusion, api, client, library, python, python3

.. container:: badges

   .. image:: https://badge.fury.io/py/yelpfusion3.svg
      :alt: PyPi
      :target: https://pypi.org/project/yelpfusion3/

   .. image:: https://dl.circleci.com/status-badge/img/gh/BenOnSocial/yelpfusion3/tree/main.svg?style=shield
      :alt: CI build

   .. image:: https://codecov.io/gh/BenOnSocial/yelpfusion3/branch/main/graph/badge.svg?token=LFX14ACT4Y
      :alt: Code Coverage
      :target: https://codecov.io/gh/BenOnSocial/yelpfusion3

   .. image:: https://readthedocs.org/projects/yelpfusion3/badge/?version=latest
      :alt: Documentation Status
      :target: https://yelpfusion3.readthedocs.io/en/latest/index.html

*yelpfusion3* is a Python 3 client library for
`Yelp Fusion API v3 <https://www.yelp.com/developers/documentation/v3/get_started>`_. The API provides Python developers
with a type-safe interface, so they do not need to process raw JSON responses.

.. note:: Tested with Python 3.9 and 3.10.

Installation
------------

.. code-block:: console

   python -m pip install --upgrade pip
   python -m pip install --upgrade yelpfusion3

Yelp API Key
------------

Sign up for a `Yelp Developers <https://www.yelp.com/developers>`_ account. Yelp's
`Authentication <https://www.yelp.com/developers/documentation/v3/authentication>`_ documentation describes how to
create a new private API key.


Basic Usage
-----------

Set the `YELP_API_KEY` environment variable to be your private API key. Setting the `YELP_API_KEY` environment variable
is currently the only supported method for supplying
your API key to the `yelpfusion3` client.

.. code-block:: python

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import BusinessDetailsEndpoint
   >>> from yelpfusion3.business.model import BusinessDetails
   >>> business_details_endpoint: BusinessDetailsEndpoint = Client.business_details(business_id="WavvLdfdP6g8aZTtbBQHTw")
   >>> business_details_endpoint
   BusinessDetailsEndpoint(business_id='WavvLdfdP6g8aZTtbBQHTw', locale=None)
   >>> business_details: BusinessDetails = business_details_endpoint.get()
   >>> business_details
   BusinessDetails(id='WavvLdfdP6g8aZTtbBQHTw', alias='gary-danko-san-francisco', name='Gary Danko', image_url=HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/eyYUz3Xl7NtcJeN7x7SQwg/o.jpg', ), is_claimed=True, is_closed=False, url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=iLXKG_naOtwkmDCMRoHImA', ), phone='+14157492060', display_phone='(415) 749-2060', review_count=5748, categories=[Category(alias='newamerican', title='American (New)'), Category(alias='french', title='French'), Category(alias='wine_bars', title='Wine Bars')], rating=4.5, location=Location(address1='800 N Point St', address2='', address3='', city='San Francisco', state='CA', zip_code='94109', country='US', display_address=['800 N Point St', 'San Francisco, CA 94109'], cross_streets=''), coordinates=Coordinates(latitude=37.80587, longitude=-122.42058), photos=[HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/eyYUz3Xl7NtcJeN7x7SQwg/o.jpg', ), HttpUrl('https://s3-media4.fl.yelpcdn.com/bphoto/1qgI44xDsgZyXxtcFgMeRQ/o.jpg', ), HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/wVGFtORjtBK8-7G-T-PmGg/o.jpg', )], price='$$$$', hours=[Hours(open=[DetailedHours(is_overnight=False, start='1700', end='2200', day=0), DetailedHours(is_overnight=False, start='1700', end='2200', day=3), DetailedHours(is_overnight=False, start='1700', end='2200', day=4), DetailedHours(is_overnight=False, start='1700', end='2200', day=5), DetailedHours(is_overnight=False, start='1700', end='2200', day=6)], hours_type='REGULAR', is_open_now=False)], transactions=[], special_hours=None)

License
-------

yelpfusion3 is released under the MIT License.
