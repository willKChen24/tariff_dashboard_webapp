from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import wits_api

#api instance
app = FastAPI()

#list of countries tariffed
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
async def get_dashboard_summary(base_country, partner_country, year, category):
    grid_data = await wits_api.get_grid_data(base_country, year, partner_country, category) #need await for API call in an async function
    
    atr = grid_data[0]
    countries_tracked = grid_data[1]
    tot_trade_vol = grid_data[2]
    htr = grid_data[3]

    #should return a JSON response
    return JSONResponse({"avg_tariff_rate" : atr, "countries_tracked" : countries_tracked, "total_trade_volume" : tot_trade_vol, "highest_tariff_rate" : htr})

#country-specific tariff data for the area below the 4 main tiles
# @app.get("/api/countries/tariffs")
# async def get_countries_tariffs(base_country, year, category, search_term):
#     if search_term and search_term in countries: #if the searched country provided and exists within the db
#         #get the data between base country and that country
#         tariff_data = get_data(base_country, year, category, search_term) #write get_data later: connect to WITS API to get the right data
#     else: #if no search term provided, display all countries with tariffs connected to base_country

#     return JSONResponse()

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

#refreshes dashboard with latest tariff data
@app.post("/api/data/refresh")
async def refresh_data():
    pass
#shows last updated status
@app.get("/api/data/status")
async def get_data_status():
    pass
#main fxn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)