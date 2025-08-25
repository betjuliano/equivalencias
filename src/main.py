import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from werkzeug.security import generate_password_hash
from src.models.equivalencia import db, Admin
from src.routes.equivalencia import equivalencia_bp
from src.config.supabase import supabase_config

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações do Flask - CORREÇÃO: Configuração adequada de sessões
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ufsm_equivalencias_2025_secret_key_admin')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'ufsm_equiv:'

# Registrar blueprints
app.register_blueprint(equivalencia_bp, url_prefix='/api')

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Usar PostgreSQL (Supabase ou outro)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Usar SQLite local (desenvolvimento)
    db_dir = os.path.join(os.path.dirname(__file__), 'database')
    os.makedirs(db_dir, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_dir, 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco de dados
db.init_app(app)

# Rota para testar conexão com Supabase
@app.route('/api/supabase/test')
def test_supabase():
    """Endpoint para testar conexão com Supabase"""
    success, message = supabase_config.test_connection()
    return jsonify({
        'success': success,
        'message': message,
        'supabase_url': supabase_config.url
    })

# Rota para informações do sistema
@app.route('/api/info')
def system_info():
    """Endpoint com informações do sistema"""
    return jsonify({
        'name': 'Sistema de Equivalências UFSM',
        'version': '2.0.1',
        'description': 'Sistema para cadastro e consulta de equivalências de disciplinas',
        'developer': 'Prof. Juliano Alves - Grupo de Pesquisa em IA - IA Projetos',
        'institution': 'Universidade Federal de Santa Maria',
        'database': 'Supabase PostgreSQL' if os.getenv('DATABASE_URL') else 'SQLite Local',
        'supabase_configured': bool(os.getenv('SUPABASE_URL')),
        'session_configured': True
    })

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
    
    # Testar conexão com Supabase
    if os.getenv('SUPABASE_URL'):
        success, message = supabase_config.test_connection()
        print(f"Supabase: {message}")

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
    
    print(f"🚀 Iniciando Sistema de Equivalências UFSM")
    print(f"📍 Porta: {port}")
    print(f"🐘 Banco: {'Supabase PostgreSQL' if os.getenv('DATABASE_URL') else 'SQLite Local'}")
    print(f"🔧 Debug: {debug}")
    print(f"🔐 Sessões: Configuradas")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

