import './Login.css';
import 'react-spotify-auth/dist/index.css';

import React from "react";
import {Scopes, SpotifyAuth} from 'react-spotify-auth';

const url = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ? "http://localhost:3001" : "";


const Login = () => {
  const clientID = '2f817bc820e7470dba54223f96f4d945';
  const redirectUri = `${url}/app`;
  const scope = [
    Scopes.userTopRead,
    Scopes.userReadPrivate,
    Scopes.userReadEmail,
    Scopes.userLibraryRead,
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


