Client Usage
============

The :py:class:`~yelpfusion3.client.Client` class provides static factory methods that create
:py:class:`~yelpfusion3.endpoint.Endpoint` objects that are used to make requests to Yelp Fusion REST endpoints. The
method parameters indicate required endpoint parameters. Optional parameters may be set on the returned
:py:class:`~yelpfusion3.endpoint.Endpoint` object.

Get detailed information about a Yelp business
----------------------------------------------

The `Business Details endpoint <https://www.yelp.com/developers/documentation/v3/business>`_ returns detailed business
content, given its unique Yelp business ID.

.. code-block:: python
   :caption: Get details for a business using its unique business ID

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import BusinessDetailsEndpoint
   >>> from yelpfusion3.business.model import BusinessDetails
   >>> business_details_endpoint: BusinessDetailsEndpoint = Client.business_details(
            business_id="WavvLdfdP6g8aZTtbBQHTw"
       )
   >>> business_details_endpoint
   BusinessDetailsEndpoint(business_id='WavvLdfdP6g8aZTtbBQHTw', locale=None)
   >>> business_details: BusinessDetails = business_details_endpoint.get()
   >>> business_details
   BusinessDetails(id='WavvLdfdP6g8aZTtbBQHTw', alias='gary-danko-san-francisco', name='Gary Danko', image_url=HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/eyYUz3Xl7NtcJeN7x7SQwg/o.jpg', ), is_claimed=True, is_closed=False, url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=iLXKG_naOtwkmDCMRoHImA', ), phone='+14157492060', display_phone='(415) 749-2060', review_count=5748, categories=[Category(alias='newamerican', title='American (New)'), Category(alias='french', title='French'), Category(alias='wine_bars', title='Wine Bars')], rating=4.5, location=Location(address1='800 N Point St', address2='', address3='', city='San Francisco', state='CA', zip_code='94109', country='US', display_address=['800 N Point St', 'San Francisco, CA 94109'], cross_streets=''), coordinates=Coordinates(latitude=37.80587, longitude=-122.42058), photos=[HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/eyYUz3Xl7NtcJeN7x7SQwg/o.jpg', ), HttpUrl('https://s3-media4.fl.yelpcdn.com/bphoto/1qgI44xDsgZyXxtcFgMeRQ/o.jpg', ), HttpUrl('https://s3-media3.fl.yelpcdn.com/bphoto/wVGFtORjtBK8-7G-T-PmGg/o.jpg', )], price='$$$$', hours=[Hours(open=[DetailedHours(is_overnight=False, start='1700', end='2200', day=0), DetailedHours(is_overnight=False, start='1700', end='2200', day=3), DetailedHours(is_overnight=False, start='1700', end='2200', day=4), DetailedHours(is_overnight=False, start='1700', end='2200', day=5), DetailedHours(is_overnight=False, start='1700', end='2200', day=6)], hours_type='REGULAR', is_open_now=False)], transactions=[], special_hours=None)

Find a Yelp business by business name and address
-------------------------------------------------

The `Business Match endpoint <https://www.yelp.com/developers/documentation/v3/business_match>`_ returns returns
detailed business content matching the given name and address.

.. code-block:: python
   :caption: Get details for a business matching the given name and address

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import BusinessMatchesEndpoint
   >>> from yelpfusion3.business.model import BusinessMatches
   >>> business_matches_endpoint: BusinessMatchesEndpoint = Client.business_matches(
            name="Gary Danko",
            address1="800 N Point St",
            city="San Francisco",
            state="CA",
            country="US",
        )
   >>> business_matches_endpoint
   BusinessMatchesEndpoint(name='Gary Danko', address1='800 N Point St', address2=None, address3=None, city='San Francisco', state='CA', country='US', latitude=None, longitude=None, phone=None, zip_code=None, yelp_business_id=None, limit=None, match_threshold=None)

   >>> business_matches: BusinessMatches = business_matches_endpoint.get()
   >>> business_matches
   BusinessMatches(businesses=[BusinessMatch(id='WavvLdfdP6g8aZTtbBQHTw', alias='gary-danko-san-francisco', name='Gary Danko', location=Location(address1='800 N Point St', address2='', address3='', city='San Francisco', state='CA', zip_code='94109', country='US', display_address=['800 N Point St', 'San Francisco, CA 94109'], cross_streets=None), coordinates=Coordinates(latitude=37.80587, longitude=-122.42058), phone='+14157492060')])

Find Yelp businesses around a given address
-------------------------------------------

The `Business Search endpoint <https://www.yelp.com/developers/documentation/v3/business_search>`_ returns up to 1,000
businesses based on the provided search criteria.

.. code-block:: python
   :caption: Find businesses within a 1,609 meter (~1 mile) radius of a given address

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import BusinessSearchEndpoint
   >>> from yelpfusion3.business.model import BusinessSearch
   >>> business_search_endpoint: BusinessSearchEndpoint = Client.business_search(location="800 N Point St, San Francisco, CA 94109")
   >>> business_search_endpoint
   BusinessSearchEndpoint(term=None, location='800 N Point St, San Francisco, CA 94109', latitude=None, longitude=None, radius=None, categories=None, locale=None, limit=None, offset=None, sort_by=None, price=None, open_now=None, open_at=None, attributes=None)
   >>> business_search_endpoint.radius = 1609
   >>> business_search_endpoint
   BusinessSearchEndpoint(term=None, location='800 N Point St, San Francisco, CA 94109', latitude=None, longitude=None, radius=1609, categories=None, locale=None, limit=None, offset=None, sort_by=None, price=None, open_now=None, open_at=None, attributes=None)
   >>> business_search: BusinessSearch = business_search_endpoint.get()
   >>> business_search
   BusinessSearch(total=668, businesses=[Business(categories=[Category(alias='newamerican', title='American (New)'), Category(alias='french', title='French'), Category(alias='wine_bars', title='Wine Bars')], coordinates=Coordinates(latitude=37.80587, longitude=-122.42058), display_phone='(415) 749-2060', distance=6.4977575238088, id='WavvLdfdP6g8aZTtbBQHTw', alias='gary-danko-san-francisco', ...

Find a Yelp business by phone number
------------------------------------

The `Phone Search endpoint <https://www.yelp.com/developers/documentation/v3/business_search_phone>`_ returns a list of
businesses based on the provided phone number.

.. code-block:: python
   :caption: Get details for a business matching the given phone number

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import PhoneSearchEndpoint
   >>> from yelpfusion3.business.model import PhoneSearch
   >>> phone_search_endpoint: PhoneSearchEndpoint = Client.phone_search(phone="+14157492060")
   >>> phone_search_endpoint
   PhoneSearchEndpoint(phone='+14157492060', locale=None)
   >>> phone_search: PhoneSearch = phone_search_endpoint.get()
   >>> phone_search
   PhoneSearch(total=2, businesses=[Business(categories=[Category(alias='newamerican', title='American (New)'), Category(alias='french', title='French'), Category(alias='wine_bars', title='Wine Bars')], coordinates=Coordinates(latitude=37.80587, longitude=-122.42058), display_phone='(415) 749-2060', distance=None, id='WavvLdfdP6g8aZTtbBQHTw', alias='gary-danko-san-francisco', image_url=HttpUrl('https://s3-media0.fl.yelpcdn.com/bphoto/eyYUz3Xl7NtcJeN7x7SQwg/o.jpg', ), is_closed=False, location=Location(address1='800 N Point St', address2='', address3='', city='San Francisco', state='CA', zip_code='94109', country='US', display_address=['800 N Point St', 'San Francisco, CA 94109'], cross_streets=None), name='Gary Danko', phone='+14157492060', price='$$$$', rating=4.5, review_count=5748, url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_phone_search&utm_source=iLXKG_naOtwkmDCMRoHImA', ), transactions=[]), Business(categories=[Category(alias='vegetarian', title='Vegetarian')], coordinates=Coordinates(latitude=43.0446128845215, longitude=-104.697525024414), display_phone='(415) 749-2060', distance=None, id='FHck1bfTw-E6RjQhnPQz2Q', alias='test-listing-lions-and-tigers-lance-creek', image_url=HttpUrl('https://s3-media0.fl.yelpcdn.com/bphoto/FcP557vFJZh1Hg3YY-Fqmw/o.jpg', ), is_closed=False, location=Location(address1=None, address2=None, address3=None, city='Lance Creek', state='WY', zip_code='82222', country='US', display_address=['Lance Creek, WY 82222'], cross_streets=None), name='TEST LISTING - Lions and Tigers', phone='+14157492060', price=None, rating=4.5, review_count=4, url=HttpUrl('https://www.yelp.com/biz/test-listing-lions-and-tigers-lance-creek?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_phone_search&utm_source=iLXKG_naOtwkmDCMRoHImA', ), transactions=[])])

Get reviews for a Yelp business
-------------------------------

The `Reviews endpoint <https://www.yelp.com/developers/documentation/v3/business_reviews>`_ returns up to three review
excerpts for a given business.

.. code-block:: python
   :caption: Get up to three review excerpts for a given business

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import ReviewsEndpoint
   >>> from yelpfusion3.business.model import Reviews
   >>> reviews_endpoint: ReviewsEndpoint = Client.reviews(business_id="WavvLdfdP6g8aZTtbBQHTw")
   >>> reviews_endpoint
   ReviewsEndpoint(business_id='WavvLdfdP6g8aZTtbBQHTw', locale=None)
   >>> reviews: Reviews = reviews_endpoint.get()
   >>> reviews
   Reviews(total=5748, possible_languages=['en', 'zh'], reviews=[Review(id='eC0QYbq3kJIlnswekVlvOg', text='It\'s been over 10 years since I\'ve dined here but the total experience and stood out so much that when friends came to town and asked for a "San Francisco...', url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&hrid=eC0QYbq3kJIlnswekVlvOg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_reviews&utm_source=iLXKG_naOtwkmDCMRoHImA', ), rating=5, time_created=datetime.datetime(2022, 9, 24, 4, 59, 34), user=User(id='8Bx7StPmiE9EQQQJSQz-ww', profile_url=HttpUrl('https://www.yelp.com/user_details?userid=8Bx7StPmiE9EQQQJSQz-ww', ), name='James T.', image_url=HttpUrl('https://s3-media4.fl.yelpcdn.com/photo/IytplDI5TB1Qi9SgDTw19Q/o.jpg', ))), Review(id='GTh70ZNWEBT3gcqUi5qcew', text="Pretty disappointed, mostly in the food. We've dined at the French laundry and other Michelin starred restaurants in CA and globally and it's quite shocking...", url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&hrid=GTh70ZNWEBT3gcqUi5qcew&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_reviews&utm_source=iLXKG_naOtwkmDCMRoHImA', ), rating=3, time_created=datetime.datetime(2022, 9, 25, 18, 59, 40), user=User(id='wvd7JQ_7ILvhdeNXoYOiZA', profile_url=HttpUrl('https://www.yelp.com/user_details?userid=wvd7JQ_7ILvhdeNXoYOiZA', ), name='Sophie L.', image_url=HttpUrl('https://s3-media2.fl.yelpcdn.com/photo/F5yjnTMcjVKVEw7Uvv7_WA/o.jpg', ))), Review(id='rGwk222b3sekNGgeHxODvw', text="It's been a couple of year since I've been to Gary Danko. My girlfriend and I were staying at the Marriott across the street for Dreamforce and I decided to...", url=HttpUrl('https://www.yelp.com/biz/gary-danko-san-francisco?adjust_creative=iLXKG_naOtwkmDCMRoHImA&hrid=rGwk222b3sekNGgeHxODvw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_reviews&utm_source=iLXKG_naOtwkmDCMRoHImA', ), rating=5, time_created=datetime.datetime(2022, 9, 23, 15, 53, 10), user=User(id='67l719uPgWQ31H8yHwaYyQ', profile_url=HttpUrl('https://www.yelp.com/user_details?userid=67l719uPgWQ31H8yHwaYyQ', ), name='Vincent T.', image_url=HttpUrl('https://s3-media1.fl.yelpcdn.com/photo/ny4-hQ9YxT_yQNW_UuMpcw/o.jpg', )))])

Find Yelp businesses that support food delivery
-----------------------------------------------

The `Transaction Search endpoint <https://www.yelp.com/developers/documentation/v3/transaction_search>`_ returns a list
of businesses which support food delivery transactions.

.. code-block:: python
   :caption: Find businesses that support food delivery transactions

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import TransactionSearchEndpoint
   >>> from yelpfusion3.business.model import TransactionSearch
   >>> transaction_search_endpoint: TransactionSearchEndpoint = Client.transaction_search(
            location="20488 Stevens Creek Blvd, Cupertino, CA 95014"
       )
   >>> transaction_search_endpoint
   TransactionSearchEndpoint(latitude=None, longitude=None, location='20488 Stevens Creek Blvd, Cupertino, CA 95014')
   >>> transaction_search: TransactionSearch = transaction_search_endpoint.get()
   >>> transaction_search
   TransactionSearch(total=3, businesses=[Business(categories=[Category(alias='delis', title='Delis'), Category(alias='soup', title='Soup'), Category(alias='sandwiches', title='Sandwiches')], coordinates=Coordinates(latitude=37.3221599, longitude=-122.01788), display_phone='(408) 973-9898', distance=None, id='TxyGY0IwDKUMAEVrM8fFGA', alias='eriks-delicafé-cupertino-4', image_url=HttpUrl('https://s3-media1.fl.yelpcdn.com/bphoto/nQZQq_UU8j28dsPeeVUPpA/o.jpg', ), is_closed=False, location=Location(address1='19652 Stevens Creek Blvd', address2='', address3='', city='Cupertino', state='CA', zip_code='95014', country='US', display_address=['19652 Stevens Creek Blvd', 'Cupertino, CA 95014'], cross_streets=None), name="Erik's DeliCafé", phone='+14089739898', price='$', rating=3.5, review_count=147, url=HttpUrl('https://www.yelp.com/biz/eriks-delicaf%C3%A9-cupertino-4?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_transactions_search_delivery&utm_source=iLXKG_naOtwkmDCMRoHImA', ), transactions=['pickup', 'delivery']), Business(categories=[Category(alias='pizza', title='Pizza')], coordinates=Coordinates(latitude=37.337301248218, longitude=-122.02272447957), display_phone='(408) 257-5555', distance=None, id='mmWu-NrA5sAy-uruf_PXxw', alias='212-new-york-pizza-cupertino-2', image_url=HttpUrl('https://s3-media1.fl.yelpcdn.com/bphoto/_JgfW0mEUAQbGeVi3mXJSg/o.jpg', ), is_closed=False, location=Location(address1='19998 Homestead Rd', address2='', address3='', city='Cupertino', state='CA', zip_code='95014', country='US', display_address=['19998 Homestead Rd', 'Cupertino, CA 95014'], cross_streets=None), name='212 New York Pizza', phone='+14082575555', price='$', rating=4.0, review_count=391, url=HttpUrl('https://www.yelp.com/biz/212-new-york-pizza-cupertino-2?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_transactions_search_delivery&utm_source=iLXKG_naOtwkmDCMRoHImA', ), transactions=['pickup', 'delivery']), Business(categories=[Category(alias='pizza', title='Pizza'), Category(alias='salad', title='Salad'), Category(alias='pastashops', title='Pasta Shops')], coordinates=Coordinates(latitude=37.2956221, longitude=-122.0320078), display_phone='(408) 973-1414', distance=None, id='QVZ_UKKkdtWHZraj4Mw5zA', alias='fast-pizza-delivery-san-jose-9', image_url=HttpUrl('https://s3-media2.fl.yelpcdn.com/bphoto/Da-o0tx3dmPRgKix4A59yQ/o.jpg', ), is_closed=False, location=Location(address1='1554 S De Anza Blvd', address2='', address3='', city='San Jose', state='CA', zip_code='95129', country='US', display_address=['1554 S De Anza Blvd', 'San Jose, CA 95129'], cross_streets=None), name='Fast Pizza Delivery', phone='+14089731414', price='$', rating=3.5, review_count=81, url=HttpUrl('https://www.yelp.com/biz/fast-pizza-delivery-san-jose-9?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_transactions_search_delivery&utm_source=iLXKG_naOtwkmDCMRoHImA', ), transactions=['pickup', 'delivery'])])

Get autocomplete suggestions for keywords, businesses, and categories
---------------------------------------------------------------------

The `Autocomplete endpoint <https://www.yelp.com/developers/documentation/v3/autocomplete>`_ returns autocomplete
suggestions for search keywords, businesses, and categories.

.. code-block:: python
   :caption: Get autocomplete suggestions for a given text input

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.business.endpoint import AutocompleteEndpoint
   >>> from yelpfusion3.business.model import Autocomplete
   >>> autocomplete_endpoint: AutocompleteEndpoint = Client.autocomplete(
            text="del", latitude=37.786942, longitude=-122.399643
       )
   >>> autocomplete_endpoint
   AutocompleteEndpoint(text='del', latitude=37.786942, longitude=-122.399643, locale=None)
   >>> autocomplete: Autocomplete = autocomplete_endpoint.get()
   >>> autocomplete
   Autocomplete(terms=[Term(text='Delivery'), Term(text='Delivery Food'), Term(text='Deli Sandwich')], businesses=[BusinessSuggestion(name='Delarosa', id='vu6PlPyKptsT6oEq50qOzA')], categories=[Category(alias='delis', title='Delis'), Category(alias='icedelivery', title='Ice Delivery'), Category(alias='waterdelivery', title='Water Delivery')])

Find Yelp events
----------------

The `Event Search endpoint <https://www.yelp.com/developers/documentation/v3/event_search>`_ returns a list of Yelp
events based on the provided search criteria.

.. code-block:: python
   :caption: Find a maximum of 3 food & drink or night life events within a 10 mile (~16,093 meters) radius around San Francisco

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.event.endpoint import EventSearchEndpoint
   >>> from yelpfusion3.event.model import EventSearch
   >>> event_search_endpoint: EventSearchEndpoint = Client.event_search()
   >>> event_search_endpoint.limit = 3
   >>> event_search_endpoint.radius = 16093
   >>> event_search_endpoint.location = "san francisco, ca"
   >>> event_search_endpoint.categories = "food-and-drink,nightlife"
   >>> event_search_endpoint
   EventSearchEndpoint(locale=None, offset=None, limit=3, sort_by=None, sort_on=None, start_date=None, end_date=None, categories='food-and-drink,nightlife', is_free=None, location='san francisco, ca', latitude=None, longitude=None, radius=16093, excluded_events=None)
   >>> event_search: EventSearch = event_search_endpoint.get()
   >>> >>> event_search
   EventSearch(total=3, events=[Event(attending_count=926, category='nightlife', cost=None, cost_max=None, description='Come join the Yelp Team and all of Yelpland in celebrating our 3rd Annual Yelp Holiday Party! Just some of the "funny, useful and cool" thrills will include...', event_site_url=HttpUrl('https://www.yelp.com/events/san-francisco-peace-love-and-yelp-our-3rd-annual-holiday-party?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_event_search&utm_source=iLXKG_naOtwkmDCMRoHImA', ), id='san-francisco-peace-love-and-yelp-our-3rd-annual-holiday-party', image_url=HttpUrl('https://s3-media2.fl.yelpcdn.com/ephoto/5Y1VFZBPHF9IIOO_IIpnhQ/o.jpg', ), interested_count=73, is_canceled=False, is_free=True, is_official=False, latitude=37.78574, longitude=-122.40255, name='Peace, Love & Yelp: Our 3rd Annual Holiday Party!', tickets_url='', time_end='2007-12-05T23:00:00-08:00', time_start='2007-12-05T20:30:00-08:00', location=Location(address1='701 Mission St', address2='', address3='', city='San Francisco', state='CA', zip_code='94103', country='US', display_address=['701 Mission St', 'San Francisco, CA 94103'], cross_streets='Opera Aly & 3rd St'), business_id='yerba-buena-center-for-the-arts-san-francisco'), Event(attending_count=1, category='food-and-drink', cost=None, cost_max=None, description="RSVP's are closed! Please await email confirmation to see if you are a lucky recipient of two tickets to this event. You can also purchase discounted...", event_site_url=HttpUrl('https://www.yelp.com/events/san-francisco-yelp-10-year-celebration-event-tickets-to-eat-drink-sf-grand-tasting?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_event_search&utm_source=iLXKG_naOtwkmDCMRoHImA', ), id='san-francisco-yelp-10-year-celebration-event-tickets-to-eat-drink-sf-grand-tasting', image_url=HttpUrl('https://s3-media1.fl.yelpcdn.com/ephoto/50h4A_wu0FmLwT0JjzIlGA/o.jpg', ), interested_count=1805, is_canceled=False, is_free=False, is_official=False, latitude=37.8062423441478, longitude=-122.428887003113, name='Yelp 10-Year Celebration Event: Tickets to Eat Drink SF Grand Tasting', tickets_url=None, time_end=None, time_start='2014-08-03T13:00:00-07:00', location=Location(address1='1 Fort Mason', address2='', address3='', city='San Francisco', state='CA', zip_code='94123', country='US', display_address=['1 Fort Mason', 'San Francisco, CA 94123'], cross_streets=''), business_id='fort-mason-san-francisco-3'), Event(attending_count=1, category='food-and-drink', cost=10.0, cost_max=None, description="Find your sea legs because on March 28th from 5:30-8pm, Hornblower Cruises & Yelp are ready to set sail on the San Francisco Bay! Hornblower's Alive After...", event_site_url=HttpUrl('https://www.yelp.com/events/san-francisco-hornblower-cruises-and-yelp-present-alive-after-five?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_event_search&utm_source=iLXKG_naOtwkmDCMRoHImA', ), id='san-francisco-hornblower-cruises-and-yelp-present-alive-after-five', image_url=HttpUrl('https://s3-media2.fl.yelpcdn.com/ephoto/rCvg_qSqteB3Gn86kqe2Vw/o.jpg', ), interested_count=984, is_canceled=False, is_free=False, is_official=True, latitude=37.7959976648205, longitude=-122.40000856452664, name='Hornblower Cruises & Yelp Present: Alive After Five!', tickets_url=None, time_end='2019-03-28T20:00:00-07:00', time_start='2019-03-28T17:30:00-07:00', location=Location(address1='Pier 3 Hornblower Lndg', address2='', address3='', city='San Francisco', state='CA', zip_code='94111', country='US', display_address=['Pier 3 Hornblower Lndg', 'San Francisco, CA 94111'], cross_streets=''), business_id='hornblower-cruises-and-events-san-francisco')])

Get detailed information about a Yelp event
-------------------------------------------

The `Event Lookup endpoint <https://www.yelp.com/developers/documentation/v3/event>`_ returns detailed information for
a Yelp event.

.. code-block:: python
   :caption: Get details for an event using its unique event ID

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.event.endpoint import EventLookupEndpoint
   >>> from yelpfusion3.event.model import Event
   >>> event_lookup_endpoint: EventLookupEndpoint = Client.event_lookup(
            event_id="oakland-saucy-oakland-restaurant-pop-up"
       )
   >>> event_lookup_endpoint
   EventLookupEndpoint(id='oakland-saucy-oakland-restaurant-pop-up', locale=None)
   >>> event: Event = event_lookup_endpoint.get()
   >>> event
   Event(attending_count=6, category='food-and-drink', cost=None, cost_max=None, description='Saucy is throwing up a pop-up restaurant party over at Anfilo Coffee! Give the menu a little peruse and then register to reserve your spot! Prices are shown...', event_site_url=HttpUrl('https://www.yelp.com/events/oakland-saucy-oakland-restaurant-pop-up?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_event_lookup&utm_source=iLXKG_naOtwkmDCMRoHImA', ), id='oakland-saucy-oakland-restaurant-pop-up', image_url=HttpUrl('https://s3-media2.fl.yelpcdn.com/ephoto/TZ0gQ1nSBVe_X4PYg44s0w/o.jpg', ), interested_count=17, is_canceled=False, is_free=False, is_official=False, latitude=37.8111486, longitude=-122.2660312, name='Saucy Oakland | Restaurant Pop-Up', tickets_url=HttpUrl('https://www.eventbrite.com/e/saucy-oakland-restaurant-pop-up-tickets-36287157866?aff=es2#tickets', ), time_end='2017-08-18T21:00:00-07:00', time_start='2017-08-18T18:00:00-07:00', location=Location(address1='35 Grand Ave', address2='', address3='', city='Oakland', state='CA', zip_code='94612', country='US', display_address=['35 Grand Ave', 'Oakland, CA 94612'], cross_streets='Broadway & Webster St'), business_id='anfilo-oakland-2')




Get detailed information about a featured Yelp event
----------------------------------------------------

The `Featured Event endpoint <https://www.yelp.com/developers/documentation/v3/featured_event>`_ returns detailed
information for the featured Yelp event for a given location.

.. code-block:: python
   :caption: Get details for a featured event

   >>> from yelpfusion3.client import Client
   >>> from yelpfusion3.event.endpoint import FeaturedEventEndpoint
   >>> from yelpfusion3.event.model import Event
   >>> featured_event_endpoint: FeaturedEventEndpoint = Client.featured_event(location="San Francisco, CA")
   >>> featured_event_endpoint
   FeaturedEventEndpoint(locale=None, location='San Francisco, CA', latitude=None, longitude=None)
   >>> event: Event = featured_event_endpoint.get()
   >>> event
   Event(attending_count=188, category='other', cost=0.0, cost_max=0.0, description="Are you ready to say #HeyToTheBay with Yelp San Francisco in November?\n\nThe #HeyToTheBay promotion is for everyone with a Yelp account!\nIt's a series of...", event_site_url=HttpUrl('https://www.yelp.com/events/san-francisco-hey-to-the-bay?adjust_creative=iLXKG_naOtwkmDCMRoHImA&utm_campaign=yelp_api_v3&utm_medium=api_v3_event_featured&utm_source=iLXKG_naOtwkmDCMRoHImA', ), id='san-francisco-hey-to-the-bay', image_url=HttpUrl('https://s3-media1.fl.yelpcdn.com/ephoto/iNj9CRV6TiC_Yz3wnpur9w/o.jpg', ), interested_count=25, is_canceled=False, is_free=False, is_official=True, latitude=37.7726402, longitude=-122.4099154, name='Hey to the Bay', tickets_url='', time_end='2022-11-14T23:30:00-08:00', time_start='2022-11-01T00:00:00-07:00', location=Location(address1='', address2='', address3='', city='San Francisco', state='CA', zip_code='94103', country='US', display_address=['San Francisco, CA 94103'], cross_streets=''), business_id='city-of-san-francisco-san-francisco')
