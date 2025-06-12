from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import wits_api

#goal: find what people already want and offer it in a faster, easier way

#api instance
app = FastAPI()

#country codes mapping (for base country dropdown menu)
country_codes = {
    "US" : "USA",
    "China" : "CHN",
    "Germany" : "DEU",
    "Japan" : "JPN",
    "Canada" : "CAN"
}

#category map (for tariff categories)
tariff_categories = {
    "all" : "ALL",
    # "Animal": "01-05_Animal",
    # "Vegetable": "06-15_Vegetable",
    # "Food Products": "16-24_FoodProd",
    # "Minerals": "25-26_Minerals",
    # "Fuels": "27-27_Fuels",
    # "Chemicals": "28-38_Chemicals",
    # "Plastic or Rubber": "39-40_PlastiRub",
    # "Hides and Skins": "41-43_HidesSkin",
    # "Wood": "44-49_Wood",
    "textiles": "50-63_TextCloth",
    # "Footwear": "64-67_Footwear",
    # "Stone and Glass": "68-71_StoneGlas",
    # "Metals": "72-83_Metals",
    "electronics": "84-85_MachElec",
    # "Transportation": "86-89_Transport",
    "automotive": "90-99_Miscellan",
    "agricultural": "AgrRaw",
    # "Chemical": "Chemical",
    # "Food": "Food",
    # "Fuel": "Fuels",
    # "Manufactures": "manuf",
    # "Ores and Metals": "OresMtls",
    # "Textiles": "Textiles",
    # "All Products": "Total",
    # "Machinery and Transport Equipment": "Transp",
    # "Raw materials": "UNCTAD-SoP1",
    # "Intermediate goods": "UNCTAD-SoP2",
    # "Consumer goods": "UNCTAD-SoP3",
    # "Capital goods": "UNCTAD-SoP4"
}


#list of countries tariffed- use for search bar function later?
countries = [
    "China",
    "Japan",
    "Russia",
    "Iran",
    "North Korea",
    "Vietnam",
    "India",
    "Turkey",
    "Brazil",
    "Argentina",
    "Indonesia",
    "Thailand",
    "Malaysia",
    "Mexico",         # some tariffs in automotive and steel sectors
    "Canada",         # historically for aluminum/steel (Section 232)
    "South Korea",    # occasionally under quota/tariff restrictions
    "European Union", # e.g., on digital services taxes or retaliation
]

#defining a path (displays the webpage)
@app.get("/")
async def shrut():
    return FileResponse("tariff_dashboard.html")

#####dashboard stats#####

#gets the data for the main 4 tiles (atr, countries tracked, total trade vol (tbd), highest tariff rate)
@app.get("/api/stats/summary")
async def get_dashboard_summary(base_country, year, category):
    partner_country = "WLD" #world aggregate data
    country_code = country_codes.get(base_country)
    product_code = tariff_categories.get(category)

    #error handling
    if not country_code:
        print("\nError: country code is invalid")
    if not product_code:
        print("\nError: produc code is invalid")

    grid_data = await wits_api.get_grid_data(country_code, year, partner_country, product_code) #need await for API call in an async function
    
    atr = grid_data[0]
    countries_tracked = grid_data[1]
    tot_trade_vol = grid_data[2]
    htr = grid_data[3]

    #should return a JSON response
    #how do we know this populates the frontend with the right data?
    return JSONResponse({"avg_tariff_rate" : atr, "countries_tracked" : countries_tracked, "total_trade_volume" : round(tot_trade_vol, 2), "highest_tariff_rate" : htr})

#country-specific tariff data for the area below the 4 main tiles
@app.get("/api/countries/tariffs")
async def get_countries_tariffs(base_country, year, category, search_term):

    #IMPORTANT: atr and htr1-3 and their categories obtained through get_tariff_data
    if search_term and search_term in countries: #if the searched country provided and exists within the db
        #get the data between base country and that ONE country
        tariff_data = await wits_api.get_tariff_data(base_country, year, category, search_term) #write get_data later: connect to WITS API to get the right data
        atr = tariff_data[0]
        top_3_tr = tariff_data[1]

        return JSONResponse({"avg_tariff_rate" : atr, "top_3_tariff_rates_&_categories" : top_3_tr})
    else: #if no search term provided, display ALL countries with tariffs connected to base_country
        pass
    # return JSONResponse()

#####filter options#####

#lists all countries with tariff data
@app.get("/api/countries/list")
async def get_countries_list():
    pass
#list all categories of tariffed goods
@app.get("/api/categories/list")
async def get_categories_list():
    pass
#gets years with available tariff data
@app.get("/api/years/available")
async def get_available_years():
    pass
#####search functionality#####

@app.get("/api/countries/search")
async def search_countries(query, base_country, year, category, limit):
    pass

#####data management#####

#refreshes dashboard with latest tariff data (automatically pulls latest data?)
@app.post("/api/data/refresh")
async def refresh_data():
    pass
#shows last updated status (don't need this for now?)
# @app.get("/api/data/status")
# async def get_data_status():
#     pass
#main fxn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)