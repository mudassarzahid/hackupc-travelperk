import './Login.css';
import 'react-spotify-auth/dist/index.css';

import {Scopes, SpotifyAuth} from 'react-spotify-auth';

const url = import.meta.env.DEV ? "http://localhost:3002" : "";


const Login = () => {
  const clientID = import.meta.env.VITE_SPOTIFY_CLIENT_ID;
  const redirectUri = `${url}/app`;
  const scope = [
    Scopes.userTopRead,
    Scopes.userReadPrivate,
    Scopes.userReadEmail,
    Scopes.userLibraryRead,
    Scopes.userReadRecentlyPlayed,
    Scopes.userModifyPlaybackState,
    Scopes.userReadCurrentlyPlaying,
    Scopes.userReadPlaybackState
  ]

  return (
    <>
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


