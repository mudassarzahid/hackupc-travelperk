import './App.css';
import './Spinner.css';

import React, {useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom';


const App = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const url = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ? "http://localhost:3000" : "";
    setIsLoading(true);

    const urlParams = new URLSearchParams(window.location.search);
    const accessTokenParam = urlParams.get('access_token');

    const fragmentWithoutHash = window.location.hash.slice(1);
    const fragmentParams = new URLSearchParams(fragmentWithoutHash);
    const accessTokenFragment = fragmentParams.get('access_token');

    const accessToken = accessTokenParam || accessTokenFragment;
    console.log(JSON.stringify({"accessToken": accessToken}))
    fetch(`${url}/api/getTracks/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"accessToken": accessToken})
    }).then(res => res.json())
      .then(userData => {
        console.log(userData);
        setUserData(userData)
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    setIsLoading(false);
  }, [navigate])


  return (<div className="App">
    {isLoading ? <>Loading</> : userData.toString()}
  </div>);
}

export default App;
