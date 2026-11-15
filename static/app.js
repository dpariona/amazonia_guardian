const BOUNDS = { south: -14.0, north: -9.0, west: -72.5, east: -68.5 };
let map;

// Inicialización del Mapa
document.addEventListener('DOMContentLoaded', () => {
    map = L.map('map').setView([-12.0, -70.5], 6);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Tiles &copy; Esri'
    }).addTo(map);
    
    L.rectangle([[BOUNDS.south, BOUNDS.west], [BOUNDS.north, BOUNDS.east]], {
      color: '#00f0ff', weight: 1.5, fillOpacity: 0.05, dashArray: '5 5'
    }).addTo(map);

    cargarDatos();
});

const detectionsLayer = L.layerGroup();

async function cargarDatos() {
  try {
    const response = await fetch('/api/detections');
    const data = await response.json();
    renderizar(data);
  } catch (error) {
    console.error("Error cargando datos:", error);
  }
}

function renderizar(rows) {
  const m = rows.filter(r => r.sensor === 'MODIS').length;
  const v = rows.filter(r => r.sensor === 'VIIRS').length;
  
  const totalEl = document.getElementById('totalCount');
  const modisEl = document.getElementById('modisCount');
  const viirsEl = document.getElementById('viirsCount');

  if(totalEl) totalEl.textContent = rows.length;
  if(modisEl) modisEl.textContent = m;
  if(viirsEl) viirsEl.textContent = v;

  detectionsLayer.clearLayers();
  
  rows.forEach(r => {
    let color = r.sensor === 'MODIS' ? '#ff6b35' : '#00f0ff';
    let radius = 7;
    
    // Pintar anomalías de color rojo y más grandes
    if (r.is_anomaly) {
        color = '#ef4444'; 
        radius = 10;       
    }

    const marker = L.circleMarker([r.latitude, r.longitude], {
      radius: radius, color: color, fillColor: color, fillOpacity: 0.8, weight: 2
    });
    
    marker.bindPopup(`<b>${r.sensor}</b><br>Date: ${r.acq_date}<br>FRP: ${r.frp} MW ${r.is_anomaly ? '<br><b style="color:red;">¡ALERTA DE ANOMALÍA!</b>' : ''}`);
    marker.addTo(detectionsLayer);
  });
  
  detectionsLayer.addTo(map);

  // Actualizar Gráfico
  const months = [...new Set(rows.map(r => r.acq_date.slice(0,7)))].sort();
  const modisData = months.map(mes => rows.filter(r => r.sensor==='MODIS' && r.acq_date.startsWith(mes)).length);
  const viirsData = months.map(mes => rows.filter(r => r.sensor==='VIIRS' && r.acq_date.startsWith(mes)).length);
  
  const canvas = document.getElementById('monthlyChart');
  if (canvas) {
      if (window.myChart) {
          window.myChart.destroy();
      }
      
      window.myChart = new Chart(canvas, {
        type: 'bar',
        data: { 
            labels: months, 
            datasets: [
              { label: 'MODIS', data: modisData, backgroundColor: '#ff6b35', borderRadius: 4 },
              { label: 'VIIRS', data: viirsData, backgroundColor: '#00f0ff', borderRadius: 4 }
            ]
        },
        options: { 
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { labels: { color: '#fff' } } 
            }, 
            scales: { 
                x: { ticks: { color: '#fff' }, grid: { color: 'rgba(255,255,255,0.1)' } }, 
                y: { ticks: { color: '#fff' }, grid: { color: 'rgba(255,255,255,0.1)' } } 
            } 
        }
      });
  }
}