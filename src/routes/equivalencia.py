from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.equivalencia import db, Equivalencia, Admin

equivalencia_bp = Blueprint('equivalencia', __name__)

# Rota para login do administrador
@equivalencia_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        session['admin_id'] = admin.id
        session['admin_username'] = admin.username
        return jsonify({'message': 'Login realizado com sucesso', 'username': admin.username}), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

# Rota para logout
@equivalencia_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

# Rota para verificar se está logado
@equivalencia_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'admin_id' in session:
        return jsonify({'authenticated': True, 'username': session.get('admin_username')}), 200
    else:
        return jsonify({'authenticated': False}), 200

# Rota pública para listar todas as equivalências
@equivalencia_bp.route('/equivalencias', methods=['GET'])
def get_equivalencias():
    try:
        equivalencias = Equivalencia.query.all()
        return jsonify([equiv.to_dict() for equiv in equivalencias]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota protegida para criar nova equivalência
@equivalencia_bp.route('/equivalencias', methods=['POST'])
def create_equivalencia():
    if 'admin_id' not in session:
        return jsonify({'error': 'Acesso negado. Login necessário.'}), 401
    
    try:
        data = request.get_json()
        
        # Validação dos campos obrigatórios
        required_fields = ['disciplina_adm', 'codigo_adm', 'ch_adm', 'disciplina_equiv', 
                          'codigo_equiv', 'curso_equiv', 'ch_equiv', 'justificativa']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        nova_equivalencia = Equivalencia(
            disciplina_adm=data['disciplina_adm'],
            codigo_adm=data['codigo_adm'],
            ch_adm=data['ch_adm'],
            disciplina_equiv=data['disciplina_equiv'],
            codigo_equiv=data['codigo_equiv'],
            curso_equiv=data['curso_equiv'],
            ch_equiv=data['ch_equiv'],
            justificativa=data['justificativa']
        )
        
        db.session.add(nova_equivalencia)
        db.session.commit()
        
        return jsonify({'message': 'Equivalência criada com sucesso', 'id': nova_equivalencia.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rota protegida para atualizar equivalência
@equivalencia_bp.route('/equivalencias/<int:id>', methods=['PUT'])
def update_equivalencia(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Acesso negado. Login necessário.'}), 401
    
    try:
        equivalencia = Equivalencia.query.get_or_404(id)
        data = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'disciplina_adm' in data:
            equivalencia.disciplina_adm = data['disciplina_adm']
        if 'codigo_adm' in data:
            equivalencia.codigo_adm = data['codigo_adm']
        if 'ch_adm' in data:
            equivalencia.ch_adm = data['ch_adm']
        if 'disciplina_equiv' in data:
            equivalencia.disciplina_equiv = data['disciplina_equiv']
        if 'codigo_equiv' in data:
            equivalencia.codigo_equiv = data['codigo_equiv']
        if 'curso_equiv' in data:
            equivalencia.curso_equiv = data['curso_equiv']
        if 'ch_equiv' in data:
            equivalencia.ch_equiv = data['ch_equiv']
        if 'justificativa' in data:
            equivalencia.justificativa = data['justificativa']
        
        db.session.commit()
        
        return jsonify({'message': 'Equivalência atualizada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rota protegida para deletar equivalência
@equivalencia_bp.route('/equivalencias/<int:id>', methods=['DELETE'])
def delete_equivalencia(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Acesso negado. Login necessário.'}), 401
    
    try:
        equivalencia = Equivalencia.query.get_or_404(id)
        db.session.delete(equivalencia)
        db.session.commit()
        
        return jsonify({'message': 'Equivalência deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

