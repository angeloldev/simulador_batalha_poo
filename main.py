#!/usr/bin/env python3
"""
Medieval Fantasy Battle Simulator
Main application entry point
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import json
from package.personagens.base import Personagem
from package.personagens.guerreiro import Guerreiro
from package.personagens.mago import Mago
from package.personagens.arqueiro import Arqueiro
from package.combate import Combate
from package.banco import BancoDados
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize data storage
banco = BancoDados()

@app.route('/')
def index():
    """Render the main page of the application"""
    personagens = banco.carregar_todos_personagens()
    return render_template('index.html', personagens=personagens)

@app.route('/create', methods=['GET', 'POST'])
def create_character():
    """Handle character creation"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        classe = request.form.get('classe')
        
        # Create character based on class selection
        if classe == 'guerreiro':
            personagem = Guerreiro(nome)
        elif classe == 'mago':
            personagem = Mago(nome)
        elif classe == 'arqueiro':
            personagem = Arqueiro(nome)
        else:
            return "Classe inválida", 400
        
        # Save the character
        banco.salvar_personagem(personagem)
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/character/<character_id>')
def view_character(character_id):
    """View character details"""
    personagem = banco.carregar_personagem(character_id)
    if not personagem:
        return "Personagem não encontrado", 404
    
    return render_template('character.html', personagem=personagem)

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    """Handle battle initialization and management"""
    personagens = banco.carregar_todos_personagens()
    
    if request.method == 'POST':
        id_personagem1 = request.form.get('personagem1')
        id_personagem2 = request.form.get('personagem2')
        
        personagem1 = banco.carregar_personagem(id_personagem1)
        personagem2 = banco.carregar_personagem(id_personagem2)
        
        if not personagem1 or not personagem2:
            return "Um ou mais personagens não encontrados", 404
            
        # Initialize combat
        combate = Combate(personagem1, personagem2)
        session['combate_id'] = combate.id
        banco.salvar_combate(combate)
        
        return redirect(url_for('battle_view', battle_id=combate.id))
    
    return render_template('battle.html', personagens=personagens)

@app.route('/battle/<battle_id>')
def battle_view(battle_id):
    """View and manage an ongoing battle"""
    combate = banco.carregar_combate(battle_id)
    if not combate:
        return "Combate não encontrado", 404
    
    return render_template('battle_view.html', combate=combate)

@app.route('/battle/<battle_id>/action', methods=['POST'])
def battle_action(battle_id):
    """Process a battle action"""
    combate = banco.carregar_combate(battle_id)
    if not combate:
        return jsonify({"error": "Combate não encontrado"}), 404
    
    action = request.form.get('action')
    habilidade_id = request.form.get('habilidade_id', None)
    
    if action == 'atacar':
        resultado = combate.executar_ataque()
    elif action == 'defender':
        resultado = combate.executar_defesa()
    elif action == 'habilidade' and habilidade_id:
        resultado = combate.usar_habilidade(habilidade_id)
    else:
        return jsonify({"error": "Ação inválida"}), 400
    
    # Check if battle is over
    if combate.finalizado:
        banco.salvar_historico_combate(combate)
    
    # Save battle state
    banco.salvar_combate(combate)
    
    return jsonify({
        "resultado": resultado,
        "personagem1": combate.personagem1.to_dict(),
        "personagem2": combate.personagem2.to_dict(),
        "turno_atual": combate.turno_atual,
        "finalizado": combate.finalizado,
        "vencedor": combate.vencedor.nome if combate.finalizado and combate.vencedor else None
    })

@app.route('/inventory/<character_id>', methods=['GET', 'POST'])
def inventory(character_id):
    """Manage character inventory"""
    personagem = banco.carregar_personagem(character_id)
    if not personagem:
        return "Personagem não encontrado", 404
    
    if request.method == 'POST':
        action = request.form.get('action')
        item_id = request.form.get('item_id')
        
        if action == 'equip':
            personagem.equipar_item(item_id)
        elif action == 'unequip':
            personagem.desequipar_item(item_id)
        elif action == 'remove':
            personagem.remover_item(item_id)
        
        banco.salvar_personagem(personagem)
        return redirect(url_for('inventory', character_id=character_id))
    
    return render_template('inventory.html', personagem=personagem)

@app.route('/history')
def battle_history():
    """View battle history"""
    historico = banco.carregar_historico_combates()
    return render_template('history.html', historico=historico)

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f"Servidor rodando em http://localhost:{port}")
    webbrowser.open(f'http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()