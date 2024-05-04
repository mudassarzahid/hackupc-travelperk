import React, {useEffect} from "react";
import { useNavigate } from "react-router-dom";

const delay = ms => new Promise(res => setTimeout(res, ms));

const App = () => {
  const navigate = useNavigate();
  const getAccessToken = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const accessTokenParam = urlParams.get('access_token');

    const fragmentWithoutHash = window.location.hash.slice(1);
    const fragmentParams = new URLSearchParams(fragmentWithoutHash);
    const accessTokenFragment = fragmentParams.get('access_token');

    return accessTokenParam || accessTokenFragment;
  }

  useEffect(() => {
    function sendToken() {
      console.log("Make request");
      console.log(document)
      //document.getElementsByTagName("button")[0].click();
      console.log(document)

      fetch("http://localhost:3000/api/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept-Type": "application/json",
        },
        body: JSON.stringify({
          "accessToken": getAccessToken()
        })
      })
        .then(result => result.json())
        .then(result => console.log(result))
    }

    sendToken()
    const interval = setInterval(() => sendToken(), 100000)
    delay(100000).then(() => navigate(-1));

    return () => {
      clearInterval(interval);
    }
  }, [])


  return <></>
}

export default App;
