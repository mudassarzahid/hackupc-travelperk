import PropTypes from 'prop-types';
import './PlayButton.css';

const PlayButton = ({ isPlaying, setIsPlaying, stopPlayback }) => {
  const label = isPlaying ? 'Stop' : 'Play';

  return (
    <div className="play-button"
         onClick={
           () => {
             let newValue = !isPlaying;
             setIsPlaying(newValue);
             if (!newValue) {
               stopPlayback();
             }
           }
         }>
      {label}
    </div>
  );
};

PlayButton.propTypes = {
  isPlaying: PropTypes.bool.isRequired,
  setIsPlaying: PropTypes.func.isRequired,
  stopPlayback: PropTypes.func.isRequired,
};

export default PlayButton;
