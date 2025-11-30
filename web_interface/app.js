document.getElementById('cityForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const city = document.getElementById('cityInput').value.trim();
    const status = document.getElementById('statusSelect').value;
    if (!city) return;
    const stationsDiv = document.getElementById('stations');
    stationsDiv.innerHTML = '<p>Buscando estações...</p>';
    try {
        let url = `http://localhost:8000/stations/city/${encodeURIComponent(city)}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erro ao buscar estações');
        const data = await response.json();
        let stations = data.results || [];
        if (status) {
            stations = stations.filter(st => st.Status === status);
        }
        if (!stations.length) {
            stationsDiv.innerHTML = '<p>Nenhuma estação encontrada para esta cidade e status.</p>';
            return;
        }
        stationsDiv.innerHTML = stations.map(st => {
            let batteryHtml = '';
            if (st.BatteryPercent !== null && st.BatteryPercent !== undefined) {
                batteryHtml = `<div><strong>Bateria:</strong> ${st.BatteryPercent.toFixed(1)}%</div>`;
            }
            let addressHtml = '';
            if (st.AddressInfo && st.AddressInfo.AddressLine1) {
                addressHtml = `<div><strong>Endereço:</strong> ${st.AddressInfo.AddressLine1}</div>`;
            }
            return `
                <div class="station">
                    <div><strong>ID:</strong> ${st.ID}</div>
                    <div><strong>Potência:</strong> ${st.Potencia} kW</div>
                    <div><strong>Status:</strong> <span class="status">${st.Status}</span></div>
                    ${batteryHtml}
                    <div><strong>Cidade:</strong> ${st.City}</div>
                    ${addressHtml}
                </div>
            `;
        }).join('');
    } catch (err) {
        stationsDiv.innerHTML = `<p>Erro: ${err.message}</p>`;
    }
});
