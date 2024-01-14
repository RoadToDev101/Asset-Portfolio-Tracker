import httpx
from app.utils.custom_exceptions import NotFoundException, BadRequestException

# TODO: Add caching to reduce API calls


def fetch_crypto_price(asset_name: str, currency: str) -> float:
    # Fetch current price from CoinGecko API
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset_name}&vs_currencies={currency}"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        if asset_name in data and currency in data[asset_name]:
            return data[asset_name][currency]
        else:
            raise NotFoundException("Price not found for the given asset and currency")
    else:
        raise BadRequestException("Failed to fetch price from CoinGecko API")


def fetch_stocks_price(asset_name: str, currency: str) -> float:
    # TODO: Implement fetching current price from Stocks API
    raise NotImplementedError("Stocks not implemented yet")


def fetch_others_price(asset_name: str, currency: str) -> float:
    # TODO: Implement fetching current price from Others API
    raise NotImplementedError("Others not implemented yet")
