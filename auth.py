"""
Sistema de Autenticação - Medieval Fantasy Battle Simulator
Módulo responsável pelo controle de usuários, registro, login e segurança.
"""

import hashlib
import secrets
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt


class User:
    """
    Classe que representa um usuário do sistema.
    """
    
    def __init__(self, user_id: int, username: str, email: str, password_hash: str, 
                 created_at: str, last_login: Optional[str] = None):
        """
        Inicializa um usuário.
        
        Args:
            user_id: ID único do usuário
            username: Nome de usuário
            email: Email do usuário
            password_hash: Hash da senha
            created_at: Data de criação da conta
            last_login: Data do último login
        """
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o usuário para dicionário (sem a senha).
        
        Returns:
            Dicionário com dados do usuário
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'last_login': self.last_login
        }


class AuthManager:
    """
    Gerenciador de autenticação responsável por todas as operações
    relacionadas a usuários e segurança.
    """
    
    def __init__(self, db_path: str = "users.db"):
        """
        Inicializa o gerenciador de autenticação.
        
        Args:
            db_path: Caminho para o banco de dados SQLite
        """
        self.db_path = db_path
        self.active_sessions = {}  # user_id -> session_token
        self._init_database()
    
    def _init_database(self) -> None:
        """
        Inicializa o banco de dados criando as tabelas necessárias.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Tabela de sessões
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def _hash_password(self, password: str) -> str:
        """
        Gera hash seguro da senha usando bcrypt.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash da senha
        """
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verifica se a senha corresponde ao hash.
        
        Args:
            password: Senha em texto plano
            password_hash: Hash armazenado
            
        Returns:
            True se a senha estiver correta
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def _generate_session_token(self) -> str:
        """
        Gera um token de sessão seguro.
        
        Returns:
            Token de sessão único
        """
        return secrets.token_urlsafe(32)
    
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Registra um novo usuário no sistema.
        
        Args:
            username: Nome de usuário
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Dicionário com resultado da operação
        """
        # Validações básicas
        if len(username) < 3:
            return {'success': False, 'message': 'Nome de usuário deve ter pelo menos 3 caracteres'}
        
        if len(password) < 6:
            return {'success': False, 'message': 'Senha deve ter pelo menos 6 caracteres'}
        
        if '@' not in email:
            return {'success': False, 'message': 'Email inválido'}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar se usuário já existe
                cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                             (username, email))
                if cursor.fetchone():
                    return {'success': False, 'message': 'Usuário ou email já existe'}
                
                # Criar hash da senha
                password_hash = self._hash_password(password)
                
                # Inserir novo usuário
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash)
                    VALUES (?, ?, ?)
                ''', (username, email, password_hash))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                return {
                    'success': True,
                    'message': 'Usuário registrado com sucesso',
                    'user_id': user_id
                }
                
        except sqlite3.Error as e:
            return {'success': False, 'message': f'Erro no banco de dados: {str(e)}'}
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autentica um usuário e cria uma sessão.
        
        Args:
            username: Nome de usuário ou email
            password: Senha em texto plano
            
        Returns:
            Dicionário com resultado da operação e token de sessão
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Buscar usuário por username ou email
                cursor.execute('''
                    SELECT id, username, email, password_hash, created_at, last_login
                    FROM users 
                    WHERE username = ? OR email = ?
                ''', (username, username))
                
                user_data = cursor.fetchone()
                if not user_data:
                    return {'success': False, 'message': 'Usuário não encontrado'}
                
                # Verificar senha
                if not self._verify_password(password, user_data[3]):
                    return {'success': False, 'message': 'Senha incorreta'}
                
                # Criar usuário
                user = User(*user_data)
                
                # Gerar token de sessão
                session_token = self._generate_session_token()
                expires_at = datetime.now() + timedelta(days=7)  # Sessão válida por 7 dias
                
                # Salvar sessão no banco
                cursor.execute('''
                    INSERT INTO sessions (user_id, session_token, expires_at)
                    VALUES (?, ?, ?)
                ''', (user.id, session_token, expires_at))
                
                # Atualizar último login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user.id,))
                
                conn.commit()
                
                # Armazenar sessão ativa
                self.active_sessions[user.id] = session_token
                
                return {
                    'success': True,
                    'message': 'Login realizado com sucesso',
                    'user': user.to_dict(),
                    'session_token': session_token
                }
                
        except sqlite3.Error as e:
            return {'success': False, 'message': f'Erro no banco de dados: {str(e)}'}
    
    def validate_session(self, session_token: str) -> Optional[User]:
        """
        Valida um token de sessão e retorna o usuário correspondente.
        
        Args:
            session_token: Token de sessão
            
        Returns:
            Objeto User se a sessão for válida, None caso contrário
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Buscar sessão válida
                cursor.execute('''
                    SELECT s.user_id, u.username, u.email, u.password_hash, 
                           u.created_at, u.last_login
                    FROM sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP
                ''', (session_token,))
                
                session_data = cursor.fetchone()
                if not session_data:
                    return None
                
                return User(*session_data)
                
        except sqlite3.Error:
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """
        Realiza logout do usuário removendo a sessão.
        
        Args:
            session_token: Token de sessão
            
        Returns:
            True se o logout foi bem-sucedido
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Remover sessão do banco
                cursor.execute('DELETE FROM sessions WHERE session_token = ?', 
                             (session_token,))
                
                # Remover das sessões ativas
                for user_id, token in list(self.active_sessions.items()):
                    if token == session_token:
                        del self.active_sessions[user_id]
                        break
                
                conn.commit()
                return True
                
        except sqlite3.Error:
            return False
    
    def cleanup_expired_sessions(self) -> None:
        """
        Remove sessões expiradas do banco de dados.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP')
                conn.commit()
        except sqlite3.Error:
            pass
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Objeto User se encontrado, None caso contrário
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, email, password_hash, created_at, last_login
                    FROM users WHERE id = ?
                ''', (user_id,))
                
                user_data = cursor.fetchone()
                if user_data:
                    return User(*user_data)
                return None
                
        except sqlite3.Error:
            return None


# Instância global do gerenciador de autenticação
auth_manager = AuthManager()