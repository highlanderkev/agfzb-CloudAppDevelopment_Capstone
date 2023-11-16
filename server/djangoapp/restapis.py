import requests
import json
from .models import CarDealer, DealerReview
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

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

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
            #print(review_result)
            sentiment = analyze_review_sentiments(review_result["review"])
            review_obj = DealerReview(dealership=review_result["dealership"], name=review_result["name"], purchase=review_result["purchase"], 
            review=review_result["review"], purchase_date=review_result["purchase_date"], car_make=review_result["car_make"], car_model=review_result["car_model"],
            car_year=review_result["car_year"], sentiment=sentiment, id=review_result["id"])
            results.append(review_obj)
    return results

def analyze_review_sentiments(text):
    """
    `analyze_review_sentiments` method to call Watson NLU and analyze text
    - Call get_request() with specified arguments
    - Get the returned sentiment label such as Positive or Negative
    """
    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    params["features"] = ["keywords","entities"]
    params["return_analyzed_text"] = True
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
    print(response)
    return response




