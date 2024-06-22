import Chart from "react-apexcharts";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { brainDataKeys } from "../../consts.jsx";
import './Chart.css';

export default function LineChart({ data }) {
    const [options, setOptions] = useState({});
    const [series, setSeries] = useState([]);

    useEffect(() => {
            setSeries(data.data);
            setOptions({
                stroke: {
                    width: 2
                },
                noData: {
                    text: "Waiting for data...",
                },
                xaxis: {
                    axisTicks: {
                        show: false,
                    },
                    categories: data.timestamp,
                    labels: {
                        trim: true,
                        show: true,
                        style: {
                            colors: ["#F1F1F1"],
                            fontSize: "12px",
                        }
                    },
                },
                yaxis: {
                    decimalsInFloat: 1,
                    forceNiceScale: true,
                },
                chart: {
                    animations: {
                        dynamicAnimation: {
                            enabled: false,
                        }
                    },
                    background: 'var(--light-black)',
                    foreColor: 'var(--light-grey)',
                    toolbar: {
                        show: false,
                    },
                },
                tooltip: {
                    enabled: true,
                    theme: "dark",
                },
                grid: {
                    show: true,
                    borderColor: "var(--light-grey)",
                    strokeDashArray: 8,
                    position: 'back',
                    yaxis: {
                        lines: {
                            show: true
                        }
                    }
                },
                column: {
                    colors: [
                        "var(--grey)",
                    ],
                    opacity: 0.2
                },
                padding: {
                    top: 0,
                    right: 24,
                    bottom: 0,
                    left: 8
                },
            });
        },
        [data]);

    return (
        <div>
            <Chart options={options}
                   series={series}
                   type="line"
                   height={440}
                   // --left-screen-width
                   width={640}/>
        </div>
    );
}


LineChart.propTypes = {
    data: PropTypes.shape({
        timestamp: PropTypes.arrayOf(PropTypes.instanceOf(Date)).isRequired,
        data: PropTypes.arrayOf(
            PropTypes.shape({
                name: PropTypes.oneOf(brainDataKeys).isRequired,
                data: PropTypes.arrayOf(PropTypes.number).isRequired,
            })
        ).isRequired,
    }).isRequired,
};

