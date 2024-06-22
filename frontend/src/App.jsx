import './App.css'
import {useEffect, useRef, useState} from "react";
import Checkbox from "./components/Checkbox/Checkbox.jsx";
import PlayButton from "./components/Buttons/PlayButton.jsx";
import Queue from "./components/Queue/Queue.jsx";
import LineChart from "./components/Graph/LineChart.jsx";
import { backendUrl, brainDataKeys, MAX_DATA_POINTS } from "./consts.jsx";
import RadarChart from "./components/Graph/RadarChart.jsx";
import Slider from "./components/Slider/Slider.jsx";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBolt } from "@fortawesome/free-solid-svg-icons";

function App() {
    const [brainData, setBrainData] = useState({
        timestamp: [],
        data: brainDataKeys.map(key => ({name: key, data: []})),
    });
    const [checkBoxData, setCheckBoxData] = useState([
        {
            "name": "Calm & Relaxing",
            "checked": false
        },
        {
            "name": "High-Energy & Adventurous",
            "checked": false
        },
        {
            "name": "Self-Exploration & Intellectual",
            "checked": false
        }
    ]);
    const [isPlaying, setIsPlaying] = useState(false);
    const [queueData, setQueueData] = useState({});
    const [audioFeatures, setAudioFeatures] = useState({radarChart: {}, tempo: undefined});
    const [selectedNum, setSelectedNum] = useState(0);
    const [sliderClicked, setSliderClicked] = useState(false);
    const [tempo, setTempo] = useState("150");
    const websocket = useRef(null);

    const stopPlayback = () => {
        websocket.current.send(JSON.stringify({
            stopPlayback: true,
        }));
    }


    const handleCheckboxChange = (index) => {
        const newCheckBoxData = [...checkBoxData];
        let newValue = !newCheckBoxData[index].checked;
        if (newValue) {
            setSelectedNum(selectedNum + 1);
        } else {
            setSelectedNum(selectedNum - 1);
        }

        newCheckBoxData[index].checked = newValue;
        setCheckBoxData(newCheckBoxData);

        if (isPlaying) {
            let allUnchecked = checkBoxData.map((item) => item.checked).every(value => value === false)
            if (allUnchecked) {
                stopPlayback();
                setIsPlaying(false);
            }
        }
    };

    useEffect(() => {
        const getAccessToken = () => {
            const urlParams = new URLSearchParams(window.location.search);
            const accessTokenParam = urlParams.get('access_token');

            const fragmentWithoutHash = window.location.hash.slice(1);
            const fragmentParams = new URLSearchParams(fragmentWithoutHash);
            const accessTokenFragment = fragmentParams.get('access_token');

            return accessTokenParam || accessTokenFragment;
        }


        const startPlayback = () => {
            websocket.current.send(JSON.stringify({
                stopPlayback: null,
                accessToken: getAccessToken(),
                checked: checkBoxData
                    .filter(element => element.checked)
                    .map(element => element.name),
                tempo: sliderClicked ? Number(tempo) : null,
            }));
        }

        if (isPlaying) {
            if (websocket.current === null) {
                console.log("Create new websocket")
                websocket.current = new WebSocket(`${backendUrl}/live-data`);
            } else {
                startPlayback();
            }

            websocket.current.onopen = () => {
                console.log('WebSocket connection opened');
                startPlayback();
            };
            websocket.current.onclose = () => {
                console.log('WebSocket connection closed');
            };
            websocket.current.onmessage = (event) => {
                const message = JSON.parse(event.data);
                switch (message.type) {
                    case 'queueData': {
                        setQueueData(message.data);
                        break;
                    }
                    case 'audioFeatures': {
                        setAudioFeatures(message.data);
                        break;
                    }
                    case 'brainStream': {
                        setBrainData((prevData) => {
                            const newTimestamps = [...prevData.timestamp, new Date(message.data.timestamp)];
                            if (newTimestamps.length > MAX_DATA_POINTS) {
                                newTimestamps.shift();
                            }

                            const newData = brainDataKeys.map(key => {
                                const prevKeyData = prevData.data.find(item => item.name === key).data;
                                const newKeyData = [...prevKeyData, message.data.data[key]];
                                if (newKeyData.length > MAX_DATA_POINTS) {
                                    newKeyData.shift();
                                }
                                return {name: key, data: newKeyData};
                            });

                            return {
                                timestamp: newTimestamps,
                                data: newData,
                            };
                        });
                    }
                }
            };

            return () => {
                // TODO
                // websocket.current.close();
            };
        }
    }, [tempo, checkBoxData, isPlaying, sliderClicked]);


    return <>
        <div className="app-container">
            <div className="left-screen-side">
                <h2>What vibe would you like to have?</h2>
                <div className="checkbox-container">
                    {
                        checkBoxData.map((item, index) => (
                            <Checkbox
                                key={item.name}
                                checked={item.checked}
                                name={item.name}
                                onChange={() => handleCheckboxChange(index)}
                            />
                        ))
                    }
                </div>

                <br/>

                <Slider
                    sliderClicked={sliderClicked}
                    setSliderClicked={setSliderClicked}
                    tempo={tempo}
                    setTempo={setTempo}
                />

                <br/>

                {
                    selectedNum > 0 ?
                        <>
                            <PlayButton
                                isPlaying={isPlaying}
                                setIsPlaying={setIsPlaying}
                                stopPlayback={stopPlayback}
                            />
                        </> : <></>
                }

                <br/><br/>

                {
                    isPlaying ?
                        brainData.timestamp.length === 0 ?
                            <>Loading Graph...</> :
                            <LineChart data={brainData}/> :
                        <></>
                }
            </div>
            {
                isPlaying ? <div className="queue-visualizations">
                        {
                            Object.keys(audioFeatures.radarChart).length > 0 ?
                                <>
                                    <RadarChart data={audioFeatures.radarChart}/>
                                    <div style={{textAlign: "center"}}>
                                        <FontAwesomeIcon icon={faBolt}/>
                                        &nbsp;
                                        <b><span style={{color: "var(--green)"}}>{audioFeatures.tempo}</span> bpm</b>
                                    </div>
                                    <br/>
                                </> :
                                <></>
                        }

                        <Queue data={queueData}/>
                    </div>
                    : <></>
            }
        </div>
    </>
}

export default App
