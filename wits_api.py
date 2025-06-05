import requests

#for testing
#for export trade values
# xprt_url = "https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/USA/year/2022/partner/WLD/product/ALL/indicator/XPRT-TRD-VL?format=JSON"
# xprt_resp = requests.get(xprt_url)
# xprt_json = xprt_resp.json()
# print(f"\nShowing export data: \n {xprt_json}")

# xprt_series = xprt_json['dataSets'][0]['series']

# #each entry in series looks like this:
# # '0:0:0:0:0': {
# #     'observations': {
# #         '0': [VALUE, 0]
# #     }
# # }

# tot_xprt_vol = 0
# for key, entry in xprt_series.items(): #entry = value
#     tot_xprt_vol += entry['observations']['0'][0]

# print(f"\nTotal Export Volume: ${round((tot_xprt_vol/1000000000), 2)}B\n")

# print("\nShowing import values\n")

# mprt_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/USA/year/2022/partner/WLD/product/ALL/indicator/MPRT-TRD-VL?format=JSON"
# mprt_resp = requests.get(mprt_url)
# mprt_json = mprt_resp.json()

# mprt_series = mprt_json['dataSets'][0]['series']

# tot_mprt_vol = 0
# for key, entry in mprt_series.items(): #entry = value
#     tot_mprt_vol += entry['observations']['0'][0]

# print(f"\nTotal Import Volume: ${round((tot_mprt_vol/1000000000), 2)}B\n")

# tot_trade_vol = tot_xprt_vol + tot_mprt_vol
# print(f"\nTotal Trade Volume: ${(tot_trade_vol//1000000000)}B\n")

# print("\nShowing tariff rates\n")

# tariffs_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-tariff/reporter/USA/year/2022/partner/WLD/product/ALL/indicator/AHS-SMPL-AVRG?format=JSON"
# tariffs_resp = requests.get(tariffs_url)
# tariffs_json = tariffs_resp.json()

# tariff_series = tariffs_json['dataSets'][0]['series']

# tariff_rates = []
# rate_ct = 0
# for key, entry in tariff_series.items():
#     tariff_rates.append(entry['observations']['0'][0])
#     rate_ct += 1

# atr = sum(tariff_rates)/rate_ct
# print(f"\nAverage Tariff Rate: {round(atr, 2)}%\n")
# print(f"Highest Tariff Rate: {round(max(tariff_rates), 2)}%\n")
# print(f"Countries tracked: {rate_ct}\n")

#returns average tariff rate, highest tariff rate, total trade volume (returns multiple vals)
async def get_grid_data(country, year, partner, product):

    #for export trade values
    xprt_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/{country}/year/{year}/partner/{partner}/product/{product}/indicator/XPRT-TRD-VL?format=JSON"
    xprt_resp = requests.get(xprt_url)
    xprt_json = xprt_resp.json()

    xprt_series = xprt_json['dataSets'][0]['series']

    # each entry in series looks like this:
    # '0:0:0:0:0': {
    #     'observations': {
    #         '0': [VALUE, 0]
    #     }
    # }

    tot_xprt_vol = 0
    for key, entry in xprt_series.items(): #entry = value
        tot_xprt_vol += entry['observations']['0'][0]

    # print(f"\nTotal Export Volume: ${round((tot_xprt_vol/1000000000), 2)}B\n")
    tot_xprt_vol = round((tot_xprt_vol/1000000000), 2)

    #for import trade values
    mprt_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/{country}/year/{year}/partner/{partner}/product/{product}/indicator/MPRT-TRD-VL?format=JSON"
    mprt_resp = requests.get(mprt_url)
    mprt_json = mprt_resp.json()

    mprt_series = mprt_json['dataSets'][0]['series']

    tot_mprt_vol = 0
    for key, entry in mprt_series.items(): #entry = value
        tot_mprt_vol += entry['observations']['0'][0]

    # print(f"\nTotal Import Volume: ${round((tot_mprt_vol/1000000000), 2)}B\n")
    tot_mprt_vol = round((tot_mprt_vol/1000000000), 2)

    #need to sum import and export trade values to get total trade vol
    tot_trade_vol = tot_xprt_vol + tot_mprt_vol
    # print(f"\nTotal Trade Volume: ${tot_trade_vol}B\n")

    #for tariff rates (non-weighted)
    tariffs_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-tariff/reporter/{country}/year/{year}/partner/{partner}/product/{product}/indicator/AHS-SMPL-AVRG?format=JSON"
    tariffs_resp = requests.get(tariffs_url)
    tariffs_json = tariffs_resp.json()

    tariff_series = tariffs_json['dataSets'][0]['series']

    tariff_rates = []
    rate_ct = 0
    for key, entry in tariff_series.items():
        tariff_rates.append(entry['observations']['0'][0])
        rate_ct += 1

    atr = round((sum(tariff_rates)/rate_ct), 2)
    htr = round(max(tariff_rates), 2)
    # print(f"\nAverage Tariff Rate: {round(atr, 2)}%\n")
    # print(f"Highest Tariff Rate: {round(max(tariff_rates), 2)}%\n")
    # print(f"Countries tracked: {rate_ct}\n")

    return atr, rate_ct, tot_trade_vol, htr


if __name__ == "__main__":
    get_grid_data("USA", 2022, "WLD", "ALL")

#how to connect wits_api and main.py?