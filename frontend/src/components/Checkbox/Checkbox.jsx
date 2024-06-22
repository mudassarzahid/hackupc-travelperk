import PropTypes from 'prop-types';
import './Checkbox.css';


const Checkbox = ({ checked, name, onChange }) => {
    let rows = name.split(" ");
    return (
        <div style={{
            textAlign: "center",
            padding: "8px",
            margin: "4px",
            borderRadius: "4px",
            boxSizing: "border-box",
            width: "100%",
            placeContent: "center",
            border: checked ? "1px solid var(--green)" : "1px solid var(--grey)",
        }}
             onClick={onChange}>
            {
                rows.map((row, i) => (
                    <div key={i}>{row}</div>
                ))
            }
        </div>
    );
};

Checkbox.propTypes = {
    checked: PropTypes.bool.isRequired,
    name: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
};

export default Checkbox;
