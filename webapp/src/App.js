import './App.css';
import './Spinner.css';

import React, {useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom';

const App = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [departureDate, setDepartureDate] = useState("2024-05-05");
  const [returnDate, setReturnDate] = useState("2024-05-05");
  const [travelBuddies, setTravelBuddies] = useState([]);
  const url = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ? "http://localhost:3000" : "";

  const handleStartDateChange = (event) => {
    setDepartureDate(event.target.value);
  }

  const handleEndDateChange = (event) => {
    setReturnDate(event.target.value);
  }

  const getAccessToken = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const accessTokenParam = urlParams.get('access_token');

    const fragmentWithoutHash = window.location.hash.slice(1);
    const fragmentParams = new URLSearchParams(fragmentWithoutHash);
    const accessTokenFragment = fragmentParams.get('access_token');

    return accessTokenParam || accessTokenFragment;
  }

  const findTravelBuddies = () => {
    fetch(`${url}/api/findTravelBuddies/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"accessToken": getAccessToken()})
    }).then(res => res.json())
      .then(userData => {
        console.log(userData);
        setIsLoading(false);
        setUserData(userData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }

  useEffect(() => {
    setIsLoading(true);

    fetch(`${url}/api/loadUserData/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"accessToken": getAccessToken()})
    }).then(res => res.json())
      .then(userData => {
        console.log(userData);
        setIsLoading(false);
        setUserData(userData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, [navigate])


  return (<div className="App">
    {
      isLoading ?
        <div>Loading...</div> :
        <div>
          <div>{userData.toString()}</div>
          <div className="mood-button">moodchanger</div>
          <div style={{display: "flex", justifyContent: "space-between"}}>
            <div>
              <div>
                <input
                  type="date"
                  id="start"
                  name="trip-start"
                  value={departureDate}
                  min="2024-05-05"
                  onChange={handleStartDateChange}
                />
                <input
                  type="date"
                  id="end"
                  name="trip-end"
                  value={returnDate}
                  min={departureDate}
                  onChange={handleEndDateChange}
                />
              </div>
              <div>
                <div className="mood-button"
                     onClick={() => findTravelBuddies()}>
                  find travel buddies
                </div>
              </div>
            </div>
            <div><img src="https://r-graph-gallery.com/img/graph/143-spider-chart-with-saveral-individuals3.png"/></div>
          </div>
        </div>
    }
  </div>);
}

export default App;
