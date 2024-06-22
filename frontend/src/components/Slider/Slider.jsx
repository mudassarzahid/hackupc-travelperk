import PropTypes from 'prop-types';
import './Slider.css';


const Slider = ({ sliderClicked, setSliderClicked, tempo, setTempo }) => {
    const display = sliderClicked ? tempo : <i>no preference</i>;

    return (
        <div
            onClick={(event) => {
                if (event.target.value === undefined) {
                    setSliderClicked(!sliderClicked);
                }
            }}
            style={{
                textAlign: "center",
                padding: "8px 8px 24px 8px",
                borderRadius: "4px",
                boxSizing: "border-box",
                width: "100%",
                placeContent: "center",
                border: sliderClicked ? "1px solid var(--green)" : "1px solid var(--grey)",
                cursor: "pointer"
            }}>
            <div style={{marginBottom: "4px"}}><b>Target bpm</b>: {display}</div>
            <input type="range"
                   className="slider"
                   min={0}
                   max={300}
                   value={tempo || ""}
                   onChange={(e) => {
                       setSliderClicked(true);
                       setTempo(e.target.value);
                   }}
                   disabled={false}/>
        </div>
    );
};

Slider.propTypes = {
    sliderClicked: PropTypes.bool.isRequired,
    setSliderClicked: PropTypes.func.isRequired,
    tempo: PropTypes.string,
    setTempo: PropTypes.func.isRequired,
};

export default Slider;
