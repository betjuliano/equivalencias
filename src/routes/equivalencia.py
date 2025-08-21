from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.equivalencia import db, Equivalencia, Admin
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

equivalencia_bp = Blueprint('equivalencia', __name__)

# Rota para login do administrador - CORRIGIDA
@equivalencia_bp.route('/login', methods=['POST'])
def login():
    try:
        logger.info("Tentativa de login recebida")
        
        # Verificar se é JSON
        if not request.is_json:
            logger.error("Request não é JSON")
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
        
        data = request.get_json()
        logger.info(f"Dados recebidos: {data}")
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logger.error("Username ou password não fornecidos")
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        logger.info(f"Tentando login para usuário: {username}")
        admin = Admin.query.filter_by(username=username).first()
        
        if not admin:
            logger.error(f"Usuário não encontrado: {username}")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        if not check_password_hash(admin.password_hash, password):
            logger.error(f"Senha incorreta para usuário: {username}")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Login bem-sucedido
        session['admin_id'] = admin.id
        session['admin_username'] = admin.username
        logger.info(f"Login bem-sucedido para usuário: {username}")
        
        return jsonify({
            'message': 'Login realizado com sucesso', 
            'username': admin.username,
            'authenticated': True
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota para logout - CORRIGIDA
@equivalencia_bp.route('/logout', methods=['POST'])
def logout():
    try:
        logger.info("Logout solicitado")
        session.clear()
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
    except Exception as e:
        logger.error(f"Erro no logout: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota para verificar se está logado - CORRIGIDA
@equivalencia_bp.route('/check-auth', methods=['GET'])
def check_auth():
    try:
        if 'admin_id' in session:
            logger.info(f"Usuário autenticado: {session.get('admin_username')}")
            return jsonify({
                'authenticated': True, 
                'username': session.get('admin_username')
            }), 200
        else:
            logger.info("Usuário não autenticado")
            return jsonify({'authenticated': False}), 200
    except Exception as e:
        logger.error(f"Erro ao verificar autenticação: {str(e)}")
        return jsonify({'authenticated': False}), 200

# Rota pública para listar todas as equivalências
@equivalencia_bp.route('/equivalencias', methods=['GET'])
def get_equivalencias():
    try:
        logger.info("Buscando equivalências")
        equivalencias = Equivalencia.query.all()
        logger.info(f"Encontradas {len(equivalencias)} equivalências")
        return jsonify([equiv.to_dict() for equiv in equivalencias]), 200
    except Exception as e:
        logger.error(f"Erro ao buscar equivalências: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Rota protegida para criar nova equivalência
@equivalencia_bp.route('/equivalencias', methods=['POST'])
def create_equivalencia():
    if 'admin_id' not in session:
        logger.warning("Tentativa de criar equivalência sem autenticação")
        return jsonify({'error': 'Acesso negado. Login necessário.'}), 401
    
    try:
        data = request.get_json()
        logger.info(f"Criando nova equivalência: {data}")
        
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
        
        logger.info(f"Equivalência criada com sucesso: ID {nova_equivalencia.id}")
        return jsonify({'message': 'Equivalência criada com sucesso', 'id': nova_equivalencia.id}), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao criar equivalência: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Rota protegida para atualizar equivalência
@equivalencia_bp.route('/equivalencias/<int:id>', methods=['PUT'])
def update_equivalencia(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Acesso negado. Login necessário.'}), 401
    
    try:
        equivalencia = Equivalencia.query.get_or_404(id)
        data = request.get_json()
        
        logger.info(f"Atualizando equivalência ID {id}: {data}")
        
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
        
        logger.info(f"Equivalência ID {id} atualizada com sucesso")
        return jsonify({'message': 'Equivalência atualizada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao atualizar equivalência ID {id}: {str(e)}")
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
        
        logger.info(f"Equivalência ID {id} deletada com sucesso")
        return jsonify({'message': 'Equivalência deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao deletar equivalência ID {id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

