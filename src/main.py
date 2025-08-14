import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from werkzeug.security import generate_password_hash
from src.models.equivalencia import db, Admin
from src.routes.equivalencia import equivalencia_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações do Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ufsm_equivalencias_2025_secret_key_admin')

# Registrar blueprints
app.register_blueprint(equivalencia_bp, url_prefix='/api')

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Usar PostgreSQL (Supabase ou outro)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Usar SQLite local (desenvolvimento)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Criar usuário administrador padrão se não existir
    if not Admin.query.filter_by(username='admin').first():
        admin_user = Admin(
            username='admin',
            password_hash=generate_password_hash('adm4125')
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário administrador criado: admin / adm4125")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

