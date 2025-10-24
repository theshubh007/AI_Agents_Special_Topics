import requests

# define a function to get exchange rate
def get_fx_rate(base: str, target: str):
        """
        Fetches the current exchange rate between two currencies.

        Args:
                base: The base currency (e.g., "SGD").
                target: The target currency (e.g., "JPY").

        Returns:
                The exchange rate information as a json response,
                or None if the rate could not be fetched.
        """
        base_url = "https://hexarate.paikama.co/api/rates/latest"
        api_url = f"{base_url}/{base}?target={target}"

        response = requests.get(api_url)
        if response.status_code == 200:
                return response.json()