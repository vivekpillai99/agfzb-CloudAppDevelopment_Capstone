import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred") 
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["allDealers"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"],city=dealer["city"],
            full_name=dealer["full_name"], id=dealer["id"], lat=dealer["lat"],
            long=dealer["long"], short_name=dealer["short_name"], st=dealer["st"],
            zip=dealer["zip"],state=dealer["state"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["docs"]
        for review in reviews:
            review_obj = DealerReview(id = review["id"], name = review["name"], dealership = review["dealership"],
            review = review["review"], purchase = review["purchase"], purchase_date = review["purchase_date"],
            car_make = review["car_make"], car_model = review["car_model"], car_year = review["car_year"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f7cb4f0a-5073-447c-9b49-d5df471efe11"
    api_key = "Zb-8zm0mTM9npFETl_JA5vscJ01G__YVfwhKmnzYsc86"
    authenticator = IAMAuthenticator(api_key) 
    nlu = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    nlu.set_service_url(url) 
    response = nlu.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label = json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return(label) 



