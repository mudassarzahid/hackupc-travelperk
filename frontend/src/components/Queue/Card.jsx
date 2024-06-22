import './Queue.css';

import PropTypes from "prop-types";

const Card = props => {
  return (
    <>
      <a href={props.link}
         target="_blank"
         rel="noreferrer">
        <div className="card-container">
          <img src={props.backgroundUrl} alt="album-image" width={48} height={48}/>
          <div className="card-content">
            <span className="card-track-text" style={{color: props.color}}>{props.text}</span>
            <span className="card-artist-text" >{props.subtext}</span>
          </div>
        </div>
      </a>
    </>
  );
};

Card.propTypes = {
  backgroundUrl: PropTypes.string.isRequired,
  link: PropTypes.string.isRequired,
  subtext: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired
};

export default Card;
