import datetime
import json
import os
import time

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cached_exchange_rate = {"rate": None, "timestamp": 0}
CACHE_EXPIRATION = 10  # Cache expiration time in seconds

LOG_FILE_PATH = "currency.json"


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


@app.get("/")
async def read_root():
    return FileResponse("index.html")


@app.post("/currency-exchange")
async def currency(request: Request):
    global cached_exchange_rate

    body = await request.json()
    source_currency = body.get("source_currency")
    destination_currency = body.get("destination_currency")

    if not source_currency or not destination_currency:
        return {
            "error": "Both source_currency and destination_currency must be provided"
        }

    if time.time() - cached_exchange_rate["timestamp"] <= CACHE_EXPIRATION:
        print("Fetched exchange rate from cache")
        return {"exchange_rate": cached_exchange_rate["rate"]}

    else:
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={source_currency}&to_currency={destination_currency}&apikey=MK1JIATPFFUM6RQZ"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            exchange_rate = float(
                data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            )

        cached_exchange_rate["rate"] = exchange_rate
        cached_exchange_rate["timestamp"] = time.time()

        log_conversion(data)

        print("Fetched exchange rate from API")
        return {"exchange_rate": exchange_rate}
