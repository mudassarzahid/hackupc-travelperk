import './Login.css';
import 'react-spotify-auth/dist/index.css';

import React, {useEffect} from "react";
import {Scopes, SpotifyAuth} from 'react-spotify-auth';

const url = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ? "http://localhost:3002" : "";


const Login = () => {
  useEffect(() => {
    function clickButton() {
      let button = document.getElementsByTagName("button")[0];
      if (button !== undefined) {
        button.click();
      } else {
        console.log(button);
      }
    }

    clickButton();
    const interval = setInterval(() => clickButton(), 100)
    return () => {
      clearInterval(interval);
    }
  }, [])

  const clientID = '2f817bc820e7470dba54223f96f4d945';
  const redirectUri = `${url}/app`;
  const scope = [
    Scopes.userTopRead,
    Scopes.userReadPrivate,
    Scopes.userReadEmail,
    Scopes.userLibraryRead,
    Scopes.userReadRecentlyPlayed,
  ]

  return (
    <>
      <div className="login-headline">Login</div>
      <div className="login-button">
        <SpotifyAuth
          redirectUri={redirectUri}
          clientID={clientID}
          scopes={scope}
        />
      </div>
    </>)
};

export default Login;


