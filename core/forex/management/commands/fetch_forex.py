import requests, csv

url = "https://www.nrb.org.np/api/forex/v1/rates"

params = {
    # "page": 1,
    "per_page": 10,#only 10 data at a request
    "from": "2026-01-01",
    "to": "2026-04-23"
}

# print(response.status_code)
with open("forex_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "Date",
        "Published_Date",
        "Currency_iso3",
        "Currency_Name",
        "Unit",
        "Buy_Rate",
        "Sell_Rate"
        ])
    writer.writeheader()

    page = 1

    while True:
        params["page"] = page#for dynamic number of pages

        response = requests.get(url, params=params)

        if (response.status_code == 200):
            forex_data = response.json()

            payload = forex_data["data"]["payload"]

            for day in payload:
                Date = day["date"]
                Published_Date = day["published_on"]

                for rate in day["rates"]:
                    Currency_Iso = rate["currency"]["iso3"]
                    Currency_Name = rate["currency"]["name"]
                    Unit = rate["currency"]["unit"]
                    Buy_Rate = rate["buy"]
                    Sell_Rate = rate["sell"]
                    writer.writerow({"Date": Date,
                                    "Published_Date": Published_Date,
                                    "Currency_iso3": Currency_Iso,
                                    "Currency_Name": Currency_Name,
                                    "Unit": Unit, "Buy_Rate": Buy_Rate,
                                    "Sell_Rate": Sell_Rate
                                    })
            
            total_pages = forex_data["pagination"]["pages"]

            if page >= total_pages:
                break

            page += 1

        else:
            print("API failed:", response.status_code)
            break
