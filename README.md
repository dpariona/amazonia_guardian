# 🛰️ Amazonia Guardian

**Amazonia Guardian** es una aplicación web desarrollada para el **NASA Space Apps Challenge 2026**, abordando el desafío [**Harmonization of MODIS and VIIRS Hot Spots**](https://www.spaceappschallenge.org/).

## 📖 Descripción del Proyecto
El objetivo del proyecto es unificar los datos satelitales de los sensores MODIS y VIIRS para monitorear y analizar la actividad de incendios en la Amazonía peruana (Madre de Dios). La plataforma permite a los administradores importar archivos CSV oficiales de NASA FIRMS, visualizar los focos de calor en un mapa interactivo y detectar anomalías de intensidad térmica (FRP).

## ✨ Características Principales
- **Gestión de Usuarios:** Registro, inicio de sesión y control de roles (Admin/Viewer).
- **Base de Datos Relacional:** Almacenamiento persistente utilizando SQLite.
- **CRUD Completo:** Panel de administración para Crear, Leer, Actualizar y Eliminar detecciones.
- **Importación de Datos:** Procesamiento automático de archivos `.csv` de la NASA (MODIS/VIIRS).
- **Visualización Interactiva:** Mapa satelital (Leaflet) con diferenciación de sensores por colores.
- **Análisis de Anomalías:** Alerta visual (puntos rojos) para focos de calor con FRP > 20 MW.
- **Gráficos Estadísticos:** Calendario de actividad mensual (Chart.js).

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3 (Diseño Premium Dark), JavaScript
- **Librerías:** Leaflet (Mapas), Chart.js (Gráficos)
- **Pruebas:** Pytest
- **Despliegue:** Render

## 🚀 Instalación y Ejecución Local
1. Clona este repositorio: `git clone https://github.com/tu-usuario/amazonia-guardian.git`
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Ejecuta la aplicación: `python app.py`
6. Abre en tu navegador: `http://127.0.0.1:5000`

## 🧪 Pruebas Automatizadas
Para ejecutar las pruebas unitarias del sistema:
```bash
pytest tests/test_app.py -v