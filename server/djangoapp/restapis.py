import requests
import json
from .models import CarDealer, DealerReview, SentimentAnalysis
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_auth_request(url, api_key, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    """
    `post_request` to make HTTP POST requests
    response = requests.post(url, params=kwargs, json=payload)
    """
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")

def get_dealers_from_cf(url, **kwargs):
    """
    Create a get_dealers_from_cf method to get dealers from a cloud function
    - Call get_request() with specified arguments
    - Parse JSON results into a CarDealer object list
    """
    results = []
    json_result = get_request(url)
    if json_result:
        for dealer in json_result:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, dealerId):
    """
    Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
    - Call get_request() with specified arguments
    - Parse JSON results into a DealerView object list
    """
    result = {}
    json_result = get_request(url, id=dealerId)
    # print(json_result)
    if json_result:
        for dealer in json_result:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            print(dealer_obj)
            result = dealer_obj
    return result


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)
    #print(json_result)
    if json_result:
        for review_result in json_result:
            # print(review_result)
            sentiment = analyze_review_sentiments(review_result["review"])
            # print(sentiment)
            if review_result["purchase"]:
                review_obj = DealerReview(dealership=review_result["dealership"], name=review_result["name"], purchase=review_result["purchase"], 
                review=review_result["review"], purchase_date=review_result["purchase_date"], car_make=review_result["car_make"], car_model=review_result["car_model"],
                car_year=review_result["car_year"], sentiment=sentiment, id=review_result["id"])
            else:
                review_obj = DealerReview(dealership=review_result["dealership"], name=review_result["name"], purchase=review_result["purchase"], 
                review=review_result["review"], purchase_date="", car_make="", car_model="",
                car_year="", sentiment=sentiment, id=review_result["id"])
            results.append(review_obj)
    return results

def analyze_review_sentiments(text):
    """
    `analyze_review_sentiments` method to call Watson NLU and analyze text
    - Call get_request() with specified arguments
    - Get the returned sentiment label such as Positive or Negative
    """
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/671f702e-3847-4e5a-ab29-e3506233f1f5/v1/analyze'
    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    params["features"] = ["sentiment"]
    params["return_analyzed_text"] = 'true'
    sentiment = None
    try:
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', 'B91e7J6X4mNhKmDI87eW8WgbNDe-o9VrmYxbNm4OsXnW'))
        json_data = json.loads(response.text)
        # print(json_data)
        if json_data['sentiment']['document']:
            sentiment = SentimentAnalysis(text, json_data['sentiment']['document']['score'], json_data['sentiment']['document']['label'])
    except:
        print("Network exception occurred")
    return sentiment

