import Card from "./Card.jsx";
import PropTypes from "prop-types";

const Queue = ({ data }) => {
    return (
        data.queue !== undefined && data.currently_playing !== undefined ? <div className="queue-container">
            <div className="queue-headline">Currently Playing</div>
            <Card
                key="currently-playing"
                color="var(--green)"
                text={data.currently_playing.name}
                link={data.currently_playing.link}
                backgroundUrl={data.currently_playing.album_image_url}
                subtext={data.currently_playing.artists.map((artist => artist.name)).join(" • ")}
            />
            <div className="queue-headline">Queue</div>
            {
                data.queue.map((item, index) => (
                    <Card
                        key={index}
                        color="var(--light-grey)"
                        text={item.name}
                        link={item.link}
                        backgroundUrl={item.album_image_url}
                        subtext={item.artists.map((artist => artist.name)).join(" • ")}
                    />
                ))
            }
        </div> : <></>
    );
};

const queueElement = {
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    artists: PropTypes.arrayOf(PropTypes.shape({
        "name": PropTypes.string.isRequired,
    })).isRequired,
    album_name: PropTypes.string.isRequired,
    album_image_url: PropTypes.string.isRequired,
    link: PropTypes.string.isRequired,
};

const queueData = {
    currently_playing: PropTypes.shape(queueElement),
    queue: PropTypes.arrayOf(PropTypes.shape(queueElement)),
};

Queue.propTypes = {
    data: PropTypes.shape(queueData).isRequired,
};

export default Queue;
