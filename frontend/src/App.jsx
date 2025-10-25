import { useEffect, useState } from 'react'
import './App.css'

function App() {
  // const [count, setCount] = useState(0)
  const [avgTariffRate, setAvgTariffRate] = useState('0.0%');
  const [totalCountries, setTotalCountries] = useState('0');
  const [totalTradeVolume, setTotalTradeVolume] = useState('$0.0B');
  const [highestTariffRate, setHighestTariffRate] = useState('0.0%');
  const [searchTerm, setSearchTerm] = useState('');
  const [lastUpdated, setLastUpdated] = useState('Never');
  const [loading, setLoading] = useState(false);

  const sampleCountries = [
      {
          name: "China",
          tariffRate: "19.3%",
          tradeVolume: "$690,600 million",
          categories: [
              { name: "Agricultural Products", rate: "15.6%" },
              { name: "Automotive", rate: "25%" },
              { name: "Electronics", rate: "11.4%" }
          ]
      },
      {
          name: "Canada",
          tariffRate: "0.1%",
          tradeVolume: "$718,900 million",
          categories: [
              { name: "Dairy Products", rate: "3.2%" },
              { name: "Textiles", rate: "0.5%" },
              { name: "Automotive", rate: "0%" }
          ]
      },
      {
          name: "Germany",
          tariffRate: "3.5%",
          tradeVolume: "$203,900 million",
          categories: [
              { name: "Automotive", rate: "10%" },
              { name: "Machinery", rate: "2.8%" },
              { name: "Chemicals", rate: "4.5%" }
          ]
      },
      {
          name: "Japan",
          tariffRate: "2.5%", 
          tradeVolume: "$216,300 million",
          categories: [
              { name: "Agricultural Products", rate: "15.1%" },
              { name: "Automotive", rate: "0%" },
              { name: "Electronics", rate: "0.4%" }
          ]
      }
  ];

  const refreshData = async () => {
    setLoading(true);

    const baseCountry = document.getElementById('base-country').value;
    const year = document.getElementById('year').value;
    const category = document.getElementById('category').value;
    
    const queryParams = `?base_country=${baseCountry}&year=${year}&category=${category}`;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/stats/summary${queryParams}`);
        
        if (!response.ok){
            throw new Error(`HTTP error- status: ${response.status}`); 
        }

        const data = await response.json();
        console.log('Received data: ', data);
        
        // Update the stat cards with real data
        setAvgTariffRate(data.avg_tariff_rate + '%');
        setTotalCountries(data.countries_tracked);
        setTotalTradeVolume('$' + data.total_trade_volume + 'B');
        setHighestTariffRate(data.highest_tariff_rate + '%');
    } catch (error){
        console.error('Error: ', error);
        // Show sample data if API fails
    } finally {
        setLoading(false);
        updateLastUpdated();
    }
  }

  const CountriesList = ({ countries }) => {
  return (
    <div className="countries-list">
      {countries.map((country) => (
        <div key={country.name} className="country-card">
          <span className="country-name">{country.name}</span>
          <span className="tariff-rate">Tariff: {country.tariffRate}</span>
          <span className="trade-volume">Trade Volume: {country.tradeVolume}</span>
          <div className="categories">
            {country.categories.map((cat) => (
              <div key={cat.name} className="category">
                <span className="category-name">{cat.name}</span>
                <span className="category-rate">{cat.rate}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
  };

  // Global function to update timestamp
  const updateLastUpdated = () => {
    const now = new Date();
    setLastUpdated(`Last updated: ${now.toLocaleString()}`);
  };

  // Initialize when DOM is ready
  const filteredCountries = sampleCountries.filter((country) =>
    country.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    refreshData();
  }, []);

  // async function countryTariffData(){
  //     document.getElementById('loading').style.display = 'block';
      
  //     const baseCountry = document.getElementById('base-country').value;
  //     const year = document.getElementById('year').value;
  //     var searchCountry = document.getElementById('search').value.toLowerCase(); //need to normalize casing here
      
  //     if (searchCountry == ""){ //search term validation moved from main to here
  //         alert("No country specified; defaulting to all");
  //         searchCountry = 'wld';
  //     }
  //     const category = 'all'; //IMPORTANT: might need to change this later?

  //     const queryParams = `?base_country=${baseCountry}&year=${year}&category=${category}&search_term=${searchCountry}`;

  //     try{
  //         const response = await fetch(`http://127.0.0.1:8000/api/countries/tariffs${queryParams}`);

  //         if(!response.ok){
  //             throw new Error(`HTTP error- status: ${response.status}`);
  //         }

  //         const data = await response.json();
  //         console.log('Received data: ', data);

  //         //IMPORTANT: data.avg_tariff_rate is the name of one of the return vals from the backend fxn
  //         document.getElementById(`tariff-rate-${searchCountry}`).textContent = data.avg_tariff_rate + "%"; 

  //         //IMPORTANT: data.top_3_tariff_rates_&_categories is a list of dics so we need to format it before returning it
  //         const top_3_categories = data.top_3_tariff_rates_and_categories.map(item => `${item.category} : ${item.tariff_rate}%`).join(', ');
  //         document.getElementById(`trade-vol-${searchCountry}`).textContent = `Top categories: ${top_3_categories}`;

  //     } catch (error){
  //         console.error('Error: ', error);
  //         // Show sample data if API fails
  //         updateLastUpdated();
  //     }
  // }

  return (
    <div>
      <div className="header">
          <h1>TariffDash- Global Tariff Dashboard</h1>
          <p>Visualization of international trade tariffs and trade volumes</p>
        </div>
      <div className="dashboard">
        <div className="controls">
            <div className="control-group">
                <label htmlFor="base-country">Base Country</label>
                <select id="base-country">
                    <option value="US">United States</option>
                    <option value="China">China</option>
                    <option value="European Union">European Union</option>
                    <option value="Japan">Japan</option>
                </select>
            </div>
      
            <div className="control-group">
                <label htmlFor="year">Year</label>
                <select id="year">
                    <option value="2022">2022</option>
                    <option value="2021">2021</option>
                    <option value="2020">2020</option>
                </select>
            </div>
            
            <div className="control-group">
                <label htmlFor="category">Category</label>
                <select id="category">
                    <option value="all">All Categories</option>
                    <option value="agricultural">Agricultural Products</option>
                    <option value="automotive">Automotive</option>
                    <option value="electronics">Electronics</option>
                    <option value="textiles">Textiles</option>
                </select>
            </div>
            
            <div className="control-group">
                <label htmlFor="search">Search Country</label>
                <input 
                  type="text" 
                  id="search" 
                  placeholder="Enter country name..." 
                  value={searchTerm} 
                  onChange={(e) => setSearchTerm(e.target.value)} 
                />
            </div>
            <button className="refresh-btn" onClick={refreshData}>Refresh Data</button>
        </div>

        <div className="stats-grid">
            <div className="stat-card">
                <div className="stat-value">{avgTariffRate}</div>
                <div className="stat-label">Average Tariff Rate</div>
            </div>
            <div className="stat-card">
                <div className="stat-value">{totalCountries}</div>
                <div className="stat-label">Countries Tracked</div>
            </div>
            <div className="stat-card">
                <div className="stat-value">{totalTradeVolume}</div>
                <div className="stat-label">Total Trade Volume</div>
            </div>
            <div className="stat-card">
                <div className="stat-value">{highestTariffRate}</div>
                <div className="stat-label">Highest Tariff Rate</div>
            </div>
        </div>
        <CountriesList countries={filteredCountries} />

        {loading && <div className="loading">Loading tariff data...</div>}
        <div className="last-updated">{lastUpdated}</div>

        {/* <!--adding a footer for contact info/socials--> */}
        <footer style={{textAlign: "center", color: "white", fontSize: "0.9rem", marginTop: "2rem"}}>
            A project by{' '}
            <a href="https://www.linkedin.com/in/will-k-chen/" target="_blank" rel="noopener noreferrer" style={{color: "#cbd5e0"}}>
              Will Chen
            </a> 
            &amp;{' '}
            <a href="https://www.linkedin.com/in/daiki-narimoto/" target="_blank" rel="noopener noreferrer" style={{color: "#cbd5e0"}}>
              Daiki Narimoto
            </a>
        </footer>
    </div>
    </div>
    )
}

export default App
