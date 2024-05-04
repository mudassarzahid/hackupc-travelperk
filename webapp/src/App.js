import React, {useEffect} from "react";

const App = () => {
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
    return () => {
      clearInterval(interval);
    }
  }, [])


  return <></>
}

export default App;
