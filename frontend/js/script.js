  // Инициализация данных
const config = {
    xMin: 0,
    xMax: 1,
    points: 1000
};

let intervals = [];
let chart = null;

// Инициализация графика
function initChart() {
    const ctx = document.getElementById('functionChart').getContext('2d');

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Лямбда 2',
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'linear',
                    position: 'center',
                    title: {
                        display: true,
                        text: 'X'
                    },
                    min: config.xMin,
                    max: config.xMax
                },
                y: {
                    title: {
                        display: true,
                        text: 'Y'
                    }
                }
            }
        }
    });

    updateChart();
}

// Обновление графика
function updateChart() {
    const defaultValue = parseFloat(document.getElementById('defaultValue').value);
    const xValues = [];
    const yValues = [];

    // Генерируем точки для графика
    for (let i = 0; i <= config.points; i++) {
        const x = config.xMin + (config.xMax - config.xMin) * i / config.points;
        xValues.push(x);
        yValues.push(calculateFunction(x, defaultValue));
    }

    // Обновляем данные графика
    chart.data.labels = xValues;
    chart.data.datasets[0].data = xValues.map((x, i) => ({x: x, y: yValues[i]}));
    chart.update();
}

// Вычисление значения функции в точке x
function calculateFunction(x, defaultValue) {
    for (const interval of intervals) {
        if (x >= interval.start && x <= interval.end) {
            return interval.value;
        }
    }
    return defaultValue;
}

// Обновление таблицы интервалов
function updateIntervalsTable() {
    const tableBody = document.getElementById('intervalsTableBody');
    tableBody.innerHTML = '';

    intervals.sort((a, b) => a.start - b.start);

    intervals.forEach((interval, index) => {
        const row = document.createElement('tr');

        const startCell = document.createElement('td');
        startCell.textContent = interval.start.toFixed(2);
        row.appendChild(startCell);

        const endCell = document.createElement('td');
        endCell.textContent = interval.end.toFixed(2);
        row.appendChild(endCell);

        const valueCell = document.createElement('td');
        valueCell.textContent = interval.value.toFixed(2);
        row.appendChild(valueCell);

        const actionCell = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Удалить';
        deleteBtn.className = 'delete-btn';
        deleteBtn.onclick = () => removeInterval(index);
        actionCell.appendChild(deleteBtn);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
    });
}

// Добавление интервала
function addInterval() {
    const start = parseFloat(document.getElementById('intervalStart').value);
    const end = parseFloat(document.getElementById('intervalEnd').value);
    const value = parseFloat(document.getElementById('intervalValue').value);

    if (start >= end) {
        alert('Начало интервала должно быть меньше конца');
        return;
    }

    intervals.push({ start, end, value });
    updateChart();
    updateIntervalsTable();
}

// Удаление интервала
function removeInterval(index) {
    intervals.splice(index, 1);
    updateChart();
    updateIntervalsTable();
}

// Обработчики событий
document.getElementById('addIntervalBtn').addEventListener('click', addInterval);
document.getElementById('defaultValue').addEventListener('input', updateChart);

// Инициализация при загрузке
window.addEventListener('DOMContentLoaded', initChart);