## Neuro Feedback Music
![Example image](/images/example.png)

## Run App

### Backend
#### Run backend
```shell
# create virtual environment & install dependencies
cd backend
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt

# run
uvicorn app.app:app --port 8000 --reload
```

### Frontend
#### Create `.env` file in `./frontend`
```shell
VITE_SPOTIFY_CLIENT_ID=''  # from Spotify Developer Dashboard 
VITE_BACKEND_WEBSOCKET_URL='ws://localhost:8000'
```
#### Run backend
```shell
# install dependencies (make sure you have NPM installed)
cd frontend
npm install --force

# run
npm run dev
```

## TODOs
- Use OpenBCI data instead of randomly generated data
- Recommendations based on multiple selects (e.g. calm & relaxing + high energy & adventurous)
