exchange_rates = {
    "USD": 0.88,
    "EUR": 0.95,
    "GBP": 1.1,
    "UAH": 0.023,
}


class Price:
    def __init__(self, value: int, currency: str, conversion_rates: dict):
        self.value: int = value
        self.currency: str = currency
        self.conversion_rates: dict = conversion_rates

    def __str__(self):
        return f"{self.value},{self.currency}"

    def convert_to(self, target_currency: str) -> "Price":
        if self.currency == target_currency:
            return self
        else:
            converted_value = (
                self.value
                / self.conversion_rates[self.currency]
                * self.conversion_rates[target_currency]
            )
            return Price(
                value=converted_value,
                currency=target_currency,
                conversion_rates=self.conversion_rates,
            )

    def __add__(self, other) -> "Price":
        converted_other = other.convert_to(self.currency)
        return Price(
            value=self.value + converted_other.value,
            currency=self.currency,
            conversion_rates=self.conversion_rates,
        )

    def __sub__(self, other) -> "Price":
        converted_other = other.convert_to(self.currency)
        return Price(
            value=self.value - converted_other.value,
            currency=self.currency,
            conversion_rates=self.conversion_rates,
        )


flight_price = Price(
    value=200, currency="USD", conversion_rates=exchange_rates
)
hotel_price = Price(
    value=1000, currency="EUR", conversion_rates=exchange_rates
)

total_price = flight_price + hotel_price
print(total_price)
