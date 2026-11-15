# 🛰️ Amazonia Guardian

**Amazonia Guardian** is a web application developed for the **NASA Space Apps Challenge 2026**, addressing the [**Harmonization of MODIS and VIIRS Hot Spots**](https://www.spaceappschallenge.org/) challenge. 

## 📖 Project Description
The goal of this project is to harmonize satellite data from the MODIS and VIIRS sensors to monitor and analyze fire activity in the Peruvian Amazon (Madre de Dios). The platform allows administrators to import official NASA FIRMS CSV files, visualize active heat spots on an interactive map, and detect thermal intensity anomalies (FRP).

## ✨ Key Features
- **User Management:** Registration, login, and role-based access control (Admin/Viewer).
- **Relational Database:** Persistent data storage using SQLite.
- **Full CRUD Operations:** Admin panel to Create, Read, Update, and Delete fire detections.
- **Data Import:** Automated processing of official NASA `.csv` files (MODIS/VIIRS).
- **Interactive Visualization:** Satellite map (Leaflet) with color-coded sensors.
- **Anomaly Detection:** Visual alerts (red markers) for high-intensity heat spots (FRP > 20 MW).
- **Statistical Charts:** Monthly fire activity calendar (Chart.js).

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite
- **Frontend:** HTML5, CSS3 (Premium Dark Theme), JavaScript
- **Libraries:** Leaflet (Maps), Chart.js (Charts)
- **Testing:** Pytest
- **Deployment:** Render

## 🚀 Local Installation & Setup
1. Clone this repository: `git clone https://github.com/dpariona/amazonia_guardian.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open in your browser: `http://127.0.0.1:5000`

## 🧪 Automated Testing
To run the unit tests for the system:
```bash
pytest tests/test_app.py -v