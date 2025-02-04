// script.js
document.addEventListener('DOMContentLoaded', function() {
    const csvInput = document.getElementById('csvFile');
    const yearSelector = document.getElementById('yearSelector');
    let globalData = null;

    csvInput.addEventListener('change', handleFileSelect);

    function handleFileSelect(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            processData(e.target.result);
        };

        reader.readAsText(file);
    }

    function processData(csv) {
        const lines = csv.split('\n');
        const headers = lines[0].split(',');
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',');
            if (values.length === headers.length) {
                const row = {};
                headers.forEach((header, index) => {
                    row[header.trim()] = values[index].trim();
                });
                data.push(row);
            }
        }

        globalData = data;
        populateYearSelector(data);
        updateSummaryStats(data);
        updateGraph(data[0]); // Mostrar primer año por defecto
    }

    function populateYearSelector(data) {
        yearSelector.innerHTML = '<option value="">Seleccione un año</option>';
        data.forEach(row => {
            const option = document.createElement('option');
            option.value = row.año;
            option.textContent = row.año;
            yearSelector.appendChild(option);
        });

        yearSelector.addEventListener('change', function() {
            const selectedData = globalData.find(row => row.año === this.value);
            if (selectedData) {
                updateGraph(selectedData);
            }
        });
    }

    function updateSummaryStats(data) {
        // Calcular promedios
        const lluviaMensualPromedio = calculateAverage(data, 'lluvia_mensual');
        const lluviaAnualPromedio = calculateAverage(data, 'lluvia_anual');
        const diasLluviaPromedio = calculateAverage(data, 'dias_lluvia');

        // Calcular tendencia comparando con 2006
        const tendencia = calculateTrend(data);

        // Actualizar DOM
        document.getElementById('lluvia-mensual').textContent = `${lluviaMensualPromedio.toFixed(1)}mm`;
        document.getElementById('lluvia-anual').textContent = `${lluviaAnualPromedio.toFixed(0)}mm`;
        document.getElementById('dias-lluvia').textContent = diasLluviaPromedio.toFixed(0);
        document.getElementById('tendencia').textContent = `${tendencia > 0 ? '+' : ''}${tendencia.toFixed(1)}%`;
    }

    function updateGraph(yearData) {
        const graphContainer = document.getElementById('rainfall-graph');
        const monthlyData = Object.entries(yearData)
            .filter(([key]) => key.startsWith('mes_'))
            .map(([_, value]) => parseFloat(value));

        // Limpiar gráfico anterior
        while (graphContainer.children.length > 1) {
            graphContainer.removeChild(graphContainer.lastChild);
        }

        // Encontrar el valor máximo para escalar las barras
        const maxValue = Math.max(...monthlyData);

        // Crear nuevas barras
        monthlyData.forEach((value, index) => {
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = `${(value / maxValue) * 100}%`;
            bar.setAttribute('data-value', `${value}mm`);
            graphContainer.appendChild(bar);
        });
    }

    function calculateAverage(data, field) {
        return data.reduce((sum, row) => sum + parseFloat(row[field]), 0) / data.length;
    }

    function calculateTrend(data) {
        const firstYear = parseFloat(data[0].lluvia_anual);
        const lastYear = parseFloat(data[data.length - 1].lluvia_anual);
        return ((lastYear - firstYear) / firstYear) * 100;
    }
});