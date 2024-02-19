import datetime
import json
import os
from dataclasses import dataclass

import requests

MIDDLE_CURRENCY = "CHF"
ALPHAVANTAGE_API_KEY = "MK1JIATPFFUM6RQZ"
LOG_FILE_PATH = "logs.json"


@dataclass
class Price:
    value: float
    currency: str

    def __str__(self):
        return f"{self.value}, {self.currency}"

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=self.value + other.value,
                currency=self.currency,
            )

        left_in_middle: float = convert(
            value=self.value,
            currency_from=self.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle + right_in_middle
        total_in_left_currency = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=self.currency,
        )
        return Price(value=total_in_left_currency, currency=self.currency)


def convert(value: float, currency_from: str, currency_to: str) -> float:
    response: requests.Response = requests.get(
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey={ALPHAVANTAGE_API_KEY}"
    )

    result: dict = response.json()

    log_conversion(result)

    coefficient: float = float(
        result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )
    return value * coefficient


def log_conversion(result: dict) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "currency_from": result["Realtime Currency Exchange Rate"][
            "1. From_Currency Code"
        ],
        "currency_to": result["Realtime Currency Exchange Rate"][
            "3. To_Currency Code"
        ],
        "rate": result["Realtime Currency Exchange Rate"]["5. Exchange Rate"],
        "timestamp": timestamp,
    }

    if not os.path.isfile(LOG_FILE_PATH):
        log_data = {"results": []}
    else:
        with open(LOG_FILE_PATH, "r") as log_file:
            log_data = json.load(log_file)

    log_data["results"].append(log_entry)

    with open(LOG_FILE_PATH, "w") as log_file:
        json.dump(log_data, log_file, indent=2)


flight = Price(value=200, currency="USD")
hotel = Price(value=1000, currency="UAH")

total = flight + hotel
print(total)
