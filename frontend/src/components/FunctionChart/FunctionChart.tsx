import React, { useState, useEffect, useRef } from 'react';
import { Chart, ChartConfiguration } from 'chart.js/auto';
import './FunctionChart.scss';

interface Interval {
    start: number;
    end: number;
    value: number;
}

type Props = {
    header: string;
}

const FunctionChart: React.FC<Props> = (props) => {
    const [defaultValue, setDefaultValue] = useState<number>(0);
    const [intervalStart, setIntervalStart] = useState<number>(0);
    const [intervalEnd, setIntervalEnd] = useState<number>(1);
    const [intervalValue, setIntervalValue] = useState<number>(1);
    const [intervals, setIntervals] = useState<Interval[]>([]);

    const chartRef = useRef<HTMLCanvasElement>(null);
    const chartInstance = useRef<Chart | null>(null);

    const config = {
        xMin: 0,
        xMax: 1,
        points: 1000
    };

    useEffect(() => {
        if (!chartRef.current) return;

        const ctx = chartRef.current.getContext('2d');
        if (!ctx) return;

        const chartConfig: ChartConfiguration = {
            type: 'line',
            data: {
                datasets: [{
                    label: props.header,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0,
                    pointRadius: 0,
                    data: []
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'center',
                        title: {
                            display: true,
                            text: 'Time'
                        },
                        min: config.xMin,
                        max: config.xMax
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    }
                }
            }
        };

        chartInstance.current = new Chart(ctx, chartConfig);

        return () => {
            if (chartInstance.current) {
                chartInstance.current.destroy();
                chartInstance.current = null;
            }
        };
    }, []);

    useEffect(() => {
        updateChart();
    }, [defaultValue, intervals]);

    const calculateFunction = (x: number, defaultValue: number): number => {
        for (const interval of intervals) {
            if (x >= interval.start && x <= interval.end) {
                return interval.value;
            }
        }
        return defaultValue;
    };

    const updateChart = () => {
        if (!chartInstance.current) return;

        const xValues: number[] = [];
        const yValues: number[] = [];

        for (let i = 0; i <= config.points; i++) {
            const x = config.xMin + (config.xMax - config.xMin) * i / config.points;
            xValues.push(x);
            yValues.push(calculateFunction(x, defaultValue));
        }

        chartInstance.current.data.labels = xValues;
        chartInstance.current.data.datasets[0].data = xValues.map((x, i) => ({x, y: yValues[i]}));
        chartInstance.current.update();
    };

    const addInterval = () => {
        const start = intervalStart;
        const end = intervalEnd;
        const value = intervalValue;

        if (start >= end) {
            alert('Начало интервала должно быть меньше конца');
            return;
        }

        setIntervals([...intervals, { start, end, value }]);
    };

    const removeInterval = (index: number) => {
        const newIntervals = [...intervals];
        newIntervals.splice(index, 1);
        setIntervals(newIntervals);
    };

    return (
        <div className="function-chart-container">
            <h1>Параметр {props.header}</h1>

            <div className="container">
                <div className="control-panel">
                    <div className="form-group">
                        <label htmlFor="defaultValue">Значение по умолчанию:</label>
                        <input
                            type="number"
                            id="defaultValue"
                            value={defaultValue}
                            step="0.1"
                            onChange={(e) => setDefaultValue(parseFloat(e.target.value))}
                        />
                    </div>

                    <h3>Добавить интервал</h3>
                    <div className="form-group">
                        <label htmlFor="intervalStart">Начало интервала:</label>
                        <input
                            type="number"
                            id="intervalStart"
                            value={intervalStart}
                            step="0.1"
                            onChange={(e) => setIntervalStart(parseFloat(e.target.value))}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="intervalEnd">Конец интервала:</label>
                        <input
                            type="number"
                            id="intervalEnd"
                            value={intervalEnd}
                            step="0.1"
                            onChange={(e) => setIntervalEnd(parseFloat(e.target.value))}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="intervalValue">Значение на интервале:</label>
                        <input
                            type="number"
                            id="intervalValue"
                            value={intervalValue}
                            step="0.1"
                            onChange={(e) => setIntervalValue(parseFloat(e.target.value))}
                        />
                    </div>
                    <button onClick={addInterval}>Добавить интервал</button>

                    <div className="intervals-table-container">
                        <h3>Список интервалов</h3>
                        <table>
                            <thead>
                            <tr>
                                <th>Начало</th>
                                <th>Конец</th>
                                <th>Значение</th>
                                <th>Действие</th>
                            </tr>
                            </thead>
                            <tbody>
                            {intervals
                                .sort((a, b) => a.start - b.start)
                                .map((interval, index) => (
                                    <tr key={index}>
                                        <td>{interval.start.toFixed(2)}</td>
                                        <td>{interval.end.toFixed(2)}</td>
                                        <td>{interval.value.toFixed(2)}</td>
                                        <td>
                                            <button
                                                className="delete-btn"
                                                onClick={() => removeInterval(index)}
                                            >
                                                Удалить
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="chart-wrapper">
                    <canvas id="functionChart" ref={chartRef}></canvas>
                </div>
            </div>
        </div>
    );
};

export default FunctionChart;