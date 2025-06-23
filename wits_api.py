import requests
import xml.etree.ElementTree as ET
#for testing 
#IMPORTANT: data past 2022 does not yet exist :/

#for products (NOT A JSON RESPONSE!)
# product_url = "https://wits.worldbank.org/API/V1/wits/datasource/trn/product/all?format=JSON"
# product_response = requests.get(product_url)

# #parse data as XML since we don't have a json response body
# root = ET.fromstring(product_response.content)

# products = []
# for product in root.findall(".//{http://wits.worldbank.org}product"):
#     code = product.attrib.get("productcode") #attrib is a dict of attributes
#     desc = product.find("{http://wits.worldbank.org}productdescription").text #finds the first child with the productdescription tag
#     products.append(desc)

# print(products)
# product_json = product_response.json()
# print(f"\nShowing all avaiable product categories: \n {product_json}")
#for export trade values
# xprt_url = "https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/USA/year/2022/partner/WLD/product/ALL/indicator/XPRT-TRD-VL?format=JSON"
# xprt_resp = requests.get(xprt_url)
# # xprt_json = xprt_resp.json()

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

# category_series = tariffs_json['structure']['dimensions']['series']
# categories = []
# for dim in category_series:
#     if dim['id'] == 'PRODUCTCODE':
#         for val in dim['values']:
#             categories.append({'id' : val['id'], 'name' : val['name']})

# for category in categories:
#     print(f"{category['id']}: {category['name']}")

# textiles_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-tariff/reporter/USA/year/2022/partner/WLD/product/Textiles/indicator/AHS-SMPL-AVRG?format=JSON"
# textiles_resp = requests.get(textiles_url)
# textiles_json = textiles_resp.json()
# print(textiles_json)
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

#more testing
tariffs_url = "https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestatstariff/reporter/usa/year/2000/partner/jpn/product/fuels/indicator/AHS-SMPL-AVRG?format=JSON"
tariffs_req = requests.get(tariffs_url)
print(f"Status: {tariffs_req.status_code}") #403, need API key?
tariffs_resp = tariffs_req.json()
print(f"\nShowing tariff data b/t US and Japan: \n{tariffs_resp}")

#returns average tariff rate, highest tariff rate, total trade volume (returns multiple vals)
def get_grid_data(country, year, partner, product):

    #for export trade values
    xprt_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestats-trade/reporter/{country}/year/{year}/partner/{partner}/product/{product}/indicator/XPRT-TRD-VL?format=JSON"
    xprt_resp = requests.get(xprt_url)
    print("EXPORT JSON:", xprt_resp.status_code, xprt_resp.text)  # DEBUG HERE
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

def get_tariff_data(base_country, year, category, search_country):

    #something wrong with this URL?
    tariffs_url = f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/tradestatstariff/reporter/{base_country}/year/{year}/partner/{search_country}/product/{category}/indicator/AHS-SMPL-AVRG?format=JSON"
    tariffs_resp = requests.get(tariffs_url)
    print(f"Status: {tariffs_resp.status_code}")
    tariffs_json = tariffs_resp.json()

    tariff_series = tariffs_json['dataSets'][0]['series']
    tariff_rates = []

    for dim in tariffs_json['structure']['dimensions']['series']:
        if dim['id'] == 'PRODUCTCODE': #isolate the product code
            product_categories = dim['values'] #this is a list of dicts with id and name
            #product_categories looks something like this:
          #{
              #"id": "84-85_MachElec",
              #"name": "Mach and Elec"
           #}
            break

    for key, entry in tariff_series.items():
        #IMPORTANT- key = FREQ : REPORTER : PARTNER : PRODUCTCODE : INDICATOR
        rate = entry["observations"]["0"][0]
        parts = key.split(':')
        category_idx = int(parts[3]) #gets PRODUCTCODE
        tariff_rates.append((rate, category_idx))

    #obtain the top 3 highest tariff rates
    tariff_rates_sorted = sorted(tariff_rates, reverse=True) #sort in descending order
    top_3_tr = tariff_rates_sorted[:3] #get the first 3 tariff rates
    atr = round((sum(tariff_rates)/len(tariff_rates)), 2)

    #obtain the respective categories for the top 3 highest tariff rates
    top_3_tr_categories = []
    for rate, idx in top_3_tr:
        category_code = product_categories[idx]["id"]
        top_3_tr_categories.append({"tariff_rate" : round(rate, 2), "category" : category_code})

    return atr, top_3_tr_categories #return atr and list with dict items

