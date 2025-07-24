# 🏰 Medieval Fantasy Battle Simulator - Sistema de Autenticação e WebSocket

Um simulador de batalha medieval com sistema completo de autenticação e comunicação em tempo real via WebSocket.

## 🚀 Funcionalidades

### 🔐 Sistema de Autenticação
- **Registro de usuários** com validação de dados
- **Login seguro** com hash de senhas (bcrypt)
- **Sessões autenticadas** com tokens seguros
- **Logout** com limpeza de sessão
- **Proteção de rotas** com decorators

### ⚡ WebSocket em Tempo Real
- **Conexões autenticadas** via WebSocket
- **Batalhas em tempo real** entre jogadores
- **Sistema de filas** para matchmaking
- **Desafios diretos** entre jogadores
- **Sincronização de estado** da batalha

### 🎮 Sistema de Jogo
- **Criação de personagens** (Guerreiro, Mago, Arqueiro)
- **Dashboard interativo** com estatísticas
- **Sala de batalha** com interface em tempo real
- **Histórico de batalhas** persistente
- **Sistema de turnos** sincronizado

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd medieval-battle-simulator
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente (opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
FLASK_ENV=development
DATABASE_URL=sqlite:///battle_simulator.db
```

## 🚀 Como Executar

### Desenvolvimento
```bash
python app.py
```

### Produção (com Gunicorn)
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app_instance.app
```

O servidor estará disponível em: `http://localhost:5000`

## 🎯 Como Usar

### 1. Primeiro Acesso
1. Acesse `http://localhost:5000`
2. Clique em "Registre-se aqui"
3. Preencha os dados:
   - **Nome de usuário**: mínimo 3 caracteres
   - **Email**: formato válido
   - **Senha**: mínimo 6 caracteres
4. Clique em "Criar Conta"

### 2. Login
1. Na página inicial, faça login com:
   - **Usuário ou Email**
   - **Senha**
2. Clique em "Entrar na Batalha"

### 3. Criar Personagem
1. No dashboard, clique em "Criar Personagem"
2. Digite o nome do seu herói
3. Escolha uma classe:
   - **🛡️ Guerreiro**: Tank resistente (Alta vida e defesa)
   - **🔮 Mago**: Dano mágico alto (Alta inteligência, baixa vida)
   - **🏹 Arqueiro**: Críticos precisos (Alta destreza, vida média)
4. Clique em "Criar Personagem"

### 4. Batalhar em Tempo Real
1. Vá para "Sala de Batalha"
2. Selecione um personagem
3. Clique em "Procurar Oponente"
4. Aguarde outro jogador entrar na fila
5. Quando a batalha começar:
   - **⚔️ Atacar**: Dano básico
   - **🛡️ Defender**: Reduz dano recebido
   - **✨ Habilidades**: Ataques especiais da classe

## 🏗️ Arquitetura do Sistema

### 📁 Estrutura de Arquivos
```
medieval-battle-simulator/
├── app.py                 # Aplicação Flask principal
├── auth.py               # Sistema de autenticação
├── requirements.txt      # Dependências Python
├── README.md            # Documentação
├── templates/           # Templates HTML
│   ├── base.html        # Template base
│   ├── login.html       # Página de login
│   ├── register.html    # Página de registro
│   ├── dashboard.html   # Dashboard principal
│   ├── create_character.html  # Criação de personagens
│   └── battle_room.html # Sala de batalha
├── static/
│   └── css/
│       └── auth.css     # Estilos CSS
├── package/             # Sistema de jogo original
│   ├── personagens/     # Classes de personagens
│   ├── banco.py         # Persistência de dados
│   └── combate.py       # Sistema de batalha
└── data/                # Dados persistidos
    ├── personagens/     # Arquivos de personagens
    ├── combates/        # Batalhas ativas
    └── historico/       # Histórico de batalhas
```

### 🔧 Componentes Principais

#### `auth.py` - Sistema de Autenticação
- **Classe `User`**: Representa um usuário do sistema
- **Classe `AuthManager`**: Gerencia todas as operações de autenticação
- **Funcionalidades**:
  - Hash seguro de senhas com bcrypt
  - Geração de tokens de sessão
  - Validação de sessões
  - Limpeza automática de sessões expiradas

#### `app.py` - Aplicação Principal
- **Classe `BattleSimulatorApp`**: Aplicação Flask integrada
- **Rotas HTTP**: Login, registro, dashboard, criação de personagens
- **WebSocket Events**: Conexão, filas de batalha, ações em tempo real
- **Middleware**: Autenticação obrigatória para rotas protegidas

### 🔒 Segurança Implementada

1. **Hash de Senhas**: bcrypt com salt automático
2. **Tokens de Sessão**: Gerados com `secrets.token_urlsafe(32)`
3. **Validação de Entrada**: Sanitização de dados do usuário
4. **Proteção CSRF**: Tokens de sessão seguros
5. **Conexões WebSocket Autenticadas**: Verificação de sessão obrigatória

### 🌐 Comunicação WebSocket

#### Eventos do Cliente → Servidor
- `join_battle_queue`: Entrar na fila de batalha
- `challenge_player`: Desafiar jogador específico
- `accept_challenge`: Aceitar desafio
- `battle_action`: Executar ação na batalha

#### Eventos do Servidor → Cliente
- `connected`: Confirmação de conexão autenticada
- `joined_queue`: Confirmação de entrada na fila
- `battle_started`: Início de batalha
- `battle_update`: Atualização do estado da batalha
- `battle_ended`: Fim da batalha

## 🎮 Classes de Personagens

### 🛡️ Guerreiro
- **Vida**: 120 (Alta resistência)
- **Força**: 15 (Dano físico alto)
- **Defesa**: 13 (Tanque resistente)
- **Recurso**: Fúria (100 pontos)
- **Habilidades**:
  - **Golpe Poderoso**: Ataque com 150% de dano
  - **Provocar**: Ganha fúria extra
  - **Postura Defensiva**: +20% defesa por 1 turno

### 🔮 Mago
- **Vida**: 80 (Baixa resistência)
- **Inteligência**: 15 (Dano mágico alto)
- **Defesa**: 6 (Frágil fisicamente)
- **Recurso**: Mana (100 pontos)
- **Habilidades**:
  - **Bola de Fogo**: Ataque elemental de fogo
  - **Raio de Gelo**: Ataque que causa lentidão
  - **Barreira Arcana**: Absorve dano por 2 turnos

### 🏹 Arqueiro
- **Vida**: 95 (Resistência média)
- **Destreza**: 15 (Precisão alta)
- **Defesa**: 8 (Defesa moderada)
- **Recurso**: Stamina (100) + Flechas (20)
- **Habilidades**:
  - **Tiro Certeiro**: +15% chance de crítico
  - **Chuva de Flechas**: Múltiplos ataques
  - **Evasão**: +30% chance de esquiva

## 🐛 Solução de Problemas

### Erro de Conexão WebSocket
```bash
# Verifique se o eventlet está instalado
pip install eventlet

# Reinicie o servidor
python app.py
```

### Erro de Banco de Dados
```bash
# Remova arquivos de banco corrompidos
rm users.db
rm -rf data/

# Reinicie a aplicação
python app.py
```

### Problemas de Dependências
```bash
# Atualize o pip
pip install --upgrade pip

# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

## 🚀 Deploy em Produção

### Usando Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "app:app_instance.app"]
```

### Usando Heroku
```bash
# Instale o Heroku CLI
# Crie um Procfile:
echo "web: gunicorn --worker-class eventlet -w 1 app:app_instance.app" > Procfile

# Deploy
heroku create seu-app-name
git push heroku main
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Desenvolvedor Principal** - Sistema de autenticação e WebSocket
- **Projeto Base** - Medieval Fantasy Battle Simulator original

## 🙏 Agradecimentos

- Flask e Flask-SocketIO pela excelente documentação
- Comunidade Python pelo suporte
- bcrypt pela segurança em hash de senhas
- Eventlet pelo suporte a WebSocket

---

**🎮 Divirta-se batalhando em Eldoria! ⚔️**