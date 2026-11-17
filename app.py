import os
import csv
import io
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Detection
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-nasa-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///amazonia.db').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor para inyectar 'lang' en todas las plantillas
@app.context_processor
def inject_lang():
    return dict(lang=session.get('lang', 'en')) # Inglés por defecto

# Ruta para cambiar el idioma
@app.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in ['en', 'es']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403
        return f(*args, **kwargs)
    return decorated_function

# ================= VISTAS WEB =================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos / Incorrect username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('El usuario ya existe / User already exists')
            return redirect(url_for('register'))
        
        is_admin = User.query.count() == 0
        new_user = User(username=request.form['username'], role='admin' if is_admin else 'viewer')
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Inicia sesión. / Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return "Acceso denegado / Access denied", 403
    return render_template('admin.html')

# ================= API REST (CRUD) =================
@app.route('/api/detections', methods=['GET'])
def get_detections():
    detections = Detection.query.all()
    return jsonify([d.to_dict() for d in detections])

@app.route('/api/detections', methods=['POST'])
@admin_required
def create_detection():
    data = request.json
    new_det = Detection(
        latitude=data.get('latitude'), longitude=data.get('longitude'),
        sensor=data.get('sensor'), confidence=data.get('confidence'),
        acq_date=data.get('acq_date'), frp=data.get('frp'),
        time=data.get('time', '1800'), satellite=data.get('satellite', 'Unknown'),
        is_anomaly=False
    )
    db.session.add(new_det)
    db.session.commit()
    return jsonify(new_det.to_dict()), 201

@app.route('/api/detections/<int:id>', methods=['PUT'])
@admin_required
def update_detection(id):
    det = Detection.query.get_or_404(id)
    data = request.json
    det.latitude = data.get('latitude', det.latitude)
    det.longitude = data.get('longitude', det.longitude)
    det.sensor = data.get('sensor', det.sensor)
    det.confidence = data.get('confidence', det.confidence)
    det.acq_date = data.get('acq_date', det.acq_date)
    db.session.commit()
    return jsonify(det.to_dict())

@app.route('/api/detections/<int:id>', methods=['DELETE'])
@admin_required
def delete_detection(id):
    det = Detection.query.get_or_404(id)
    db.session.delete(det)
    db.session.commit()
    return jsonify({"message": "Eliminado correctamente / Successfully deleted"}), 200

# ================= UPLOAD CSV =================
@app.route('/upload_csv', methods=['POST'])
@admin_required
def upload_csv():
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo / No file selected.')
        return redirect(url_for('admin_panel'))
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        flash('Archivo no válido. Debe ser un .csv / Invalid file. Must be a .csv file.')
        return redirect(url_for('admin_panel'))

    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        nuevas_detecciones = []
        for row in csv_input:
            if 'latitude' in row and 'longitude' in row:
                frp_val = float(row.get('frp', 0) or 0)
                
                # Lógica de Anomalía (FRP > 20 MW)
                es_anomalia = False
                if frp_val > 20.0:
                    es_anomalia = True
                    
                nueva = Detection(
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    sensor=row.get('instrument', 'MODIS').upper(), 
                    confidence=row.get('confidence', 'nominal'),
                    acq_date=row.get('acq_date', '2026-10-01'),
                    frp=frp_val,
                    time=row.get('acq_time', '1200'),
                    satellite=row.get('satellite', 'Unknown'),
                    is_anomaly=es_anomalia
                )
                nuevas_detecciones.append(nueva)
        
        db.session.add_all(nuevas_detecciones)
        db.session.commit()
        flash(f'¡Éxito! Se importaron {len(nuevas_detecciones)} detecciones / Successfully imported {len(nuevas_detecciones)} detections.')
        
    except Exception as e:
        flash(f'Error al procesar el archivo / Error processing file: {str(e)}')
        
    return redirect(url_for('admin_panel'))

# Inicializar Base de Datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)