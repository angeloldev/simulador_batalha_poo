"""
Aplicação Principal - Medieval Fantasy Battle Simulator
Servidor Flask com WebSocket e sistema de autenticação integrado.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from functools import wraps
import os
from datetime import datetime
from auth import auth_manager, User
from package.banco import BancoDados
from package.personagens.guerreiro import Guerreiro
from package.personagens.mago import Mago
from package.personagens.arqueiro import Arqueiro
from package.combate import Combate


class BattleSimulatorApp:
    """
    Classe principal da aplicação que integra Flask, SocketIO e o sistema de batalha.
    """
    
    def __init__(self):
        """
        Inicializa a aplicação Flask com todas as configurações necessárias.
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.app.config['SESSION_COOKIE_SECURE'] = False  # True em produção com HTTPS
        self.app.config['SESSION_COOKIE_HTTPONLY'] = True
        self.app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        
        # Inicializar SocketIO
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Inicializar banco de dados do jogo
        self.banco = BancoDados()
        
        # Salas de batalha ativas (room_id -> battle_data)
        self.active_battles = {}
        
        # Usuários conectados (user_id -> socket_id)
        self.connected_users = {}
        
        self._setup_routes()
        self._setup_socket_events()
    
    def require_auth(self, f):
        """
        Decorator para rotas que requerem autenticação.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_token = session.get('session_token')
            if not session_token:
                return redirect(url_for('login'))
            
            user = auth_manager.validate_session(session_token)
            if not user:
                session.clear()
                flash('Sessão expirada. Faça login novamente.', 'warning')
                return redirect(url_for('login'))
            
            # Adicionar usuário ao contexto da requisição
            request.current_user = user
            return f(*args, **kwargs)
        
        return decorated_function
    
    def _setup_routes(self):
        """
        Configura todas as rotas da aplicação.
        """
        
        @self.app.route('/')
        def index():
            """Página inicial - redireciona para dashboard se autenticado."""
            session_token = session.get('session_token')
            if session_token and auth_manager.validate_session(session_token):
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            """Página de login."""
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '')
                
                if not username or not password:
                    flash('Por favor, preencha todos os campos.', 'error')
                    return render_template('login.html')
                
                result = auth_manager.login_user(username, password)
                
                if result['success']:
                    session['session_token'] = result['session_token']
                    session['user_id'] = result['user']['id']
                    session['username'] = result['user']['username']
                    flash(f'Bem-vindo, {result["user"]["username"]}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash(result['message'], 'error')
            
            return render_template('login.html')
        
        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            """Página de registro."""
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                confirm_password = request.form.get('confirm_password', '')
                
                if not all([username, email, password, confirm_password]):
                    flash('Por favor, preencha todos os campos.', 'error')
                    return render_template('register.html')
                
                if password != confirm_password:
                    flash('As senhas não coincidem.', 'error')
                    return render_template('register.html')
                
                result = auth_manager.register_user(username, email, password)
                
                if result['success']:
                    flash('Conta criada com sucesso! Faça login para continuar.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash(result['message'], 'error')
            
            return render_template('register.html')
        
        @self.app.route('/logout')
        def logout():
            """Logout do usuário."""
            session_token = session.get('session_token')
            if session_token:
                auth_manager.logout_user(session_token)
            
            session.clear()
            flash('Logout realizado com sucesso.', 'info')
            return redirect(url_for('login'))
        
        @self.app.route('/dashboard')
        @self.require_auth
        def dashboard():
            """Dashboard principal do usuário autenticado."""
            user = request.current_user
            
            # Buscar personagens do usuário
            personagens = self.banco.carregar_todos_personagens()
            user_characters = [p for p in personagens if hasattr(p, 'owner_id') and p.owner_id == user.id]
            
            return render_template('dashboard.html', 
                                 user=user, 
                                 personagens=user_characters,
                                 total_characters=len(user_characters))
        
        @self.app.route('/create_character', methods=['GET', 'POST'])
        @self.require_auth
        def create_character():
            """Criação de personagens."""
            if request.method == 'POST':
                nome = request.form.get('nome', '').strip()
                classe = request.form.get('classe', '')
                
                if not nome or not classe:
                    flash('Por favor, preencha todos os campos.', 'error')
                    return render_template('create_character.html')
                
                # Criar personagem baseado na classe
                if classe == 'guerreiro':
                    personagem = Guerreiro(nome)
                elif classe == 'mago':
                    personagem = Mago(nome)
                elif classe == 'arqueiro':
                    personagem = Arqueiro(nome)
                else:
                    flash('Classe inválida.', 'error')
                    return render_template('create_character.html')
                
                # Associar personagem ao usuário
                personagem.owner_id = request.current_user.id
                
                # Salvar personagem
                if self.banco.salvar_personagem(personagem):
                    flash(f'Personagem {nome} criado com sucesso!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Erro ao criar personagem.', 'error')
            
            return render_template('create_character.html')
        
        @self.app.route('/battle_room')
        @self.require_auth
        def battle_room():
            """Sala de batalha em tempo real."""
            return render_template('battle_room.html', user=request.current_user)
        
        @self.app.route('/api/characters')
        @self.require_auth
        def api_characters():
            """API para listar personagens do usuário."""
            personagens = self.banco.carregar_todos_personagens()
            user_characters = [
                p.to_dict() for p in personagens 
                if hasattr(p, 'owner_id') and p.owner_id == request.current_user.id
            ]
            return jsonify(user_characters)
    
    def _setup_socket_events(self):
        """
        Configura todos os eventos WebSocket.
        """
        
        @self.socketio.on('connect')
        def handle_connect():
            """Evento de conexão WebSocket."""
            # Verificar autenticação
            session_token = session.get('session_token')
            if not session_token:
                disconnect()
                return False
            
            user = auth_manager.validate_session(session_token)
            if not user:
                disconnect()
                return False
            
            # Registrar usuário conectado
            self.connected_users[user.id] = request.sid
            
            emit('connected', {
                'message': f'Conectado como {user.username}',
                'user_id': user.id,
                'username': user.username
            })
            
            print(f'Usuário {user.username} conectado via WebSocket')
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Evento de desconexão WebSocket."""
            # Remover usuário da lista de conectados
            for user_id, socket_id in list(self.connected_users.items()):
                if socket_id == request.sid:
                    del self.connected_users[user_id]
                    print(f'Usuário {user_id} desconectado')
                    break
        
        @self.socketio.on('join_battle_queue')
        def handle_join_battle_queue(data):
            """Usuário entra na fila de batalha."""
            session_token = session.get('session_token')
            user = auth_manager.validate_session(session_token)
            
            if not user:
                emit('error', {'message': 'Não autenticado'})
                return
            
            character_id = data.get('character_id')
            if not character_id:
                emit('error', {'message': 'ID do personagem não fornecido'})
                return
            
            # Buscar personagem
            personagem = self.banco.carregar_personagem(character_id)
            if not personagem or not hasattr(personagem, 'owner_id') or personagem.owner_id != user.id:
                emit('error', {'message': 'Personagem não encontrado ou não pertence ao usuário'})
                return
            
            # Adicionar à sala de espera
            join_room('battle_queue')
            
            emit('joined_queue', {
                'message': 'Procurando oponente...',
                'character': personagem.to_dict()
            })
            
            # Notificar outros usuários na fila
            emit('player_joined_queue', {
                'user': user.username,
                'character': personagem.to_dict()
            }, room='battle_queue', include_self=False)
        
        @self.socketio.on('challenge_player')
        def handle_challenge_player(data):
            """Desafiar outro jogador para batalha."""
            session_token = session.get('session_token')
            user = auth_manager.validate_session(session_token)
            
            if not user:
                emit('error', {'message': 'Não autenticado'})
                return
            
            target_user_id = data.get('target_user_id')
            character_id = data.get('character_id')
            
            if target_user_id not in self.connected_users:
                emit('error', {'message': 'Jogador não está online'})
                return
            
            # Buscar personagem do desafiante
            personagem = self.banco.carregar_personagem(character_id)
            if not personagem or personagem.owner_id != user.id:
                emit('error', {'message': 'Personagem inválido'})
                return
            
            # Enviar desafio para o jogador alvo
            target_socket_id = self.connected_users[target_user_id]
            emit('battle_challenge', {
                'challenger': user.username,
                'challenger_id': user.id,
                'character': personagem.to_dict()
            }, room=target_socket_id)
        
        @self.socketio.on('accept_challenge')
        def handle_accept_challenge(data):
            """Aceitar desafio de batalha."""
            session_token = session.get('session_token')
            user = auth_manager.validate_session(session_token)
            
            if not user:
                emit('error', {'message': 'Não autenticado'})
                return
            
            challenger_id = data.get('challenger_id')
            character_id = data.get('character_id')
            
            if challenger_id not in self.connected_users:
                emit('error', {'message': 'Desafiante não está mais online'})
                return
            
            # Buscar personagens
            personagem1 = self.banco.carregar_personagem(data.get('challenger_character_id'))
            personagem2 = self.banco.carregar_personagem(character_id)
            
            if not personagem1 or not personagem2:
                emit('error', {'message': 'Erro ao carregar personagens'})
                return
            
            # Criar batalha
            combate = Combate(personagem1, personagem2)
            battle_room_id = f"battle_{combate.id}"
            
            # Armazenar batalha ativa
            self.active_battles[battle_room_id] = {
                'combate': combate,
                'player1_id': challenger_id,
                'player2_id': user.id,
                'player1_socket': self.connected_users[challenger_id],
                'player2_socket': self.connected_users[user.id]
            }
            
            # Adicionar jogadores à sala da batalha
            join_room(battle_room_id)
            join_room(battle_room_id, room=self.connected_users[challenger_id])
            
            # Notificar início da batalha
            emit('battle_started', {
                'battle_id': combate.id,
                'room_id': battle_room_id,
                'combate': combate.obter_resumo_combate()
            }, room=battle_room_id)
        
        @self.socketio.on('battle_action')
        def handle_battle_action(data):
            """Processar ação de batalha."""
            session_token = session.get('session_token')
            user = auth_manager.validate_session(session_token)
            
            if not user:
                emit('error', {'message': 'Não autenticado'})
                return
            
            battle_room_id = data.get('room_id')
            action = data.get('action')
            
            if battle_room_id not in self.active_battles:
                emit('error', {'message': 'Batalha não encontrada'})
                return
            
            battle_data = self.active_battles[battle_room_id]
            combate = battle_data['combate']
            
            # Verificar se é o turno do jogador
            if combate.personagem_ativo.owner_id != user.id:
                emit('error', {'message': 'Não é seu turno'})
                return
            
            # Executar ação
            resultado = None
            if action == 'atacar':
                resultado = combate.executar_ataque()
            elif action == 'defender':
                resultado = combate.executar_defesa()
            elif action == 'habilidade':
                habilidade_id = data.get('habilidade_id')
                if habilidade_id:
                    resultado = combate.usar_habilidade(habilidade_id)
            
            if resultado:
                # Atualizar estado da batalha
                battle_update = {
                    'action_result': resultado,
                    'combate': combate.obter_resumo_combate()
                }
                
                # Enviar atualização para ambos os jogadores
                emit('battle_update', battle_update, room=battle_room_id)
                
                # Verificar se a batalha terminou
                if combate.finalizado:
                    # Salvar no histórico
                    self.banco.salvar_historico_combate(combate)
                    
                    # Remover batalha ativa
                    del self.active_battles[battle_room_id]
                    
                    # Notificar fim da batalha
                    emit('battle_ended', {
                        'winner': combate.vencedor.nome if combate.vencedor else None,
                        'combate': combate.obter_resumo_combate()
                    }, room=battle_room_id)
    
    def run(self, debug=True, host='127.0.0.1', port=5000):
        """
        Inicia o servidor da aplicação.
        
        Args:
            debug: Modo debug
            host: Host do servidor
            port: Porta do servidor
        """
        print(f"🚀 Iniciando Medieval Fantasy Battle Simulator")
        print(f"📡 Servidor rodando em http://{host}:{port}")
        print(f"🔐 Sistema de autenticação ativo")
        print(f"⚡ WebSocket habilitado para batalhas em tempo real")
        
        # Limpar sessões expiradas
        auth_manager.cleanup_expired_sessions()
        
        self.socketio.run(self.app, debug=debug, host=host, port=port)


# Criar instância da aplicação
app_instance = BattleSimulatorApp()

if __name__ == '__main__':
    app_instance.run(debug=True)