import requests
from django.core.exceptions import ValidationError


def validator_isin(isin: str) -> None:
    url = f"https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={isin}"

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise ValidationError(f"HTTP error occurred while validating ISIN: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise ValidationError(
            f"Request error occurred while validating ISIN: {req_err}")


def validator_interest_rate(value):
    if value < 0 or value > 100:
        raise ValidationError('Interest rate must be between 0 and 100 percent.')
