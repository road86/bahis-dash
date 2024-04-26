import requests
import pandas as pd
from typing import Union


class KoboDataFetcher:
    def __init__(self, api_token: str, form_id: str):
        self.api_token = api_token
        self.form_id = form_id
        self.base_url = "http://kf.sharful.com/api/v2/assets/a73VCS5ESwG3UgkfvfC2K2/data.json"  # data/a73VCS5ESwG3UgkfvfC2K2/"  # a73VCS5ESwG3UgkfvfC2K2

    def fetch_data(self) -> Union[pd.DataFrame, dict]:
        # API endpoint for fetching form submissions
        url = f"{self.base_url}{self.form_id}"

        # Make a GET request with authentication
        headers = {"Authorization": f"Token {self.api_token}"}
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()

            # Check if the response contains submission data
            if "results" in response_data:
                form_submissions = response_data["results"]

                # Convert submission data to DataFrame
                df = pd.DataFrame(form_submissions)

                return df
            else:
                return response_data  # Return metadata dictionary
        else:
            return {"error": f"Failed to fetch form submissions. Status code: {response.status_code}"}


# Example usage:
api_token = "0197ea51807b2909bc64d846f18babd607281086"
form_id = ""  # "a73VCS5ESwG3UgkfvfC2K2"
data_fetcher = KoboDataFetcher(api_token, form_id)
result = data_fetcher.fetch_data()

# Check the type of the result and handle accordingly
if isinstance(result, pd.DataFrame):
    print("DataFrame:")
    print(result)
elif isinstance(result, dict):
    print("Dictionary:")
    print(result)
