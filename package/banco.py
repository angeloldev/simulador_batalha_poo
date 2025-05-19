"""
Database module for the Medieval Fantasy Battle Simulator.
Handles data serialization, loading, and persistence.
"""

import os
import json
import pickle
from typing import Dict, Any, List, Optional, Union
import uuid
from package.personagens.base import Personagem
from package.personagens.guerreiro import Guerreiro
from package.personagens.mago import Mago
from package.personagens.arqueiro import Arqueiro
from package.combate import Combate


class BancoDados:
    """
    Database class for managing game data persistence.
    """
    
    def __init__(self, usar_pickle: bool = False):
        """
        Initialize the database
        
        Args:
            usar_pickle: Whether to use pickle for serialization (True) or JSON (False)
        """
        self.usar_pickle = usar_pickle
        
        # Ensure data directories exist
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.personagens_dir = os.path.join(self.data_dir, "personagens")
        self.combates_dir = os.path.join(self.data_dir, "combates")
        self.historico_dir = os.path.join(self.data_dir, "historico")
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.personagens_dir, exist_ok=True)
        os.makedirs(self.combates_dir, exist_ok=True)
        os.makedirs(self.historico_dir, exist_ok=True)
    
    def _obter_caminho_personagem(self, personagem_id: str) -> str:
        """
        Get the file path for a character
        
        Args:
            personagem_id: Character ID
            
        Returns:
            File path for the character
        """
        ext = ".pkl" if self.usar_pickle else ".json"
        return os.path.join(self.personagens_dir, f"{personagem_id}{ext}")
    
    def _obter_caminho_combate(self, combate_id: str) -> str:
        """
        Get the file path for a combat
        
        Args:
            combate_id: Combat ID
            
        Returns:
            File path for the combat
        """
        ext = ".pkl" if self.usar_pickle else ".json"
        return os.path.join(self.combates_dir, f"{combate_id}{ext}")
    
    def _obter_caminho_historico(self, combate_id: str) -> str:
        """
        Get the file path for a combat history
        
        Args:
            combate_id: Combat ID
            
        Returns:
            File path for the combat history
        """
        ext = ".pkl" if self.usar_pickle else ".json"
        return os.path.join(self.historico_dir, f"{combate_id}{ext}")
    
    def _classe_para_objeto(self, data: Dict[str, Any]) -> Personagem:
        """
        Convert class name to appropriate character object
        
        Args:
            data: Character data dictionary
            
        Returns:
            Character instance of appropriate class
        """
        if data["classe"] == "Guerreiro":
            return Guerreiro.from_dict(data)
        elif data["classe"] == "Mago":
            return Mago.from_dict(data)
        elif data["classe"] == "Arqueiro":
            return Arqueiro.from_dict(data)
        else:
            raise ValueError(f"Classe não suportada: {data['classe']}")
    
    def salvar_personagem(self, personagem: Personagem) -> bool:
        """
        Save a character to file
        
        Args:
            personagem: Character to save
            
        Returns:
            True if successful, False otherwise
        """
        caminho = self._obter_caminho_personagem(personagem.id)
        
        try:
            if self.usar_pickle:
                with open(caminho, 'wb') as arquivo:
                    pickle.dump(personagem, arquivo)
            else:
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    json.dump(personagem.to_dict(), arquivo, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar personagem: {e}")
            return False
    
    def carregar_personagem(self, personagem_id: str) -> Optional[Personagem]:
        """
        Load a character from file
        
        Args:
            personagem_id: ID of the character to load
            
        Returns:
            The loaded character if found, None otherwise
        """
        caminho = self._obter_caminho_personagem(personagem_id)
        
        if not os.path.exists(caminho):
            return None
        
        try:
            if self.usar_pickle:
                with open(caminho, 'rb') as arquivo:
                    return pickle.load(arquivo)
            else:
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    data = json.load(arquivo)
                    return self._classe_para_objeto(data)
        except Exception as e:
            print(f"Erro ao carregar personagem: {e}")
            return None
    
    def carregar_todos_personagens(self) -> List[Personagem]:
        """
        Load all characters from files
        
        Returns:
            List of all characters
        """
        personagens = []
        
        ext = ".pkl" if self.usar_pickle else ".json"
        for arquivo in os.listdir(self.personagens_dir):
            if arquivo.endswith(ext):
                personagem_id = arquivo[:-len(ext)]
                personagem = self.carregar_personagem(personagem_id)
                if personagem:
                    personagens.append(personagem)
        
        return personagens
    
    def excluir_personagem(self, personagem_id: str) -> bool:
        """
        Delete a character file
        
        Args:
            personagem_id: ID of the character to delete
            
        Returns:
            True if successful, False otherwise
        """
        caminho = self._obter_caminho_personagem(personagem_id)
        
        if not os.path.exists(caminho):
            return False
        
        try:
            os.remove(caminho)
            return True
        except Exception as e:
            print(f"Erro ao excluir personagem: {e}")
            return False
    
    def salvar_combate(self, combate: Combate) -> bool:
        """
        Save a combat to file
        
        Args:
            combate: Combat to save
            
        Returns:
            True if successful, False otherwise
        """
        caminho = self._obter_caminho_combate(combate.id)
        
        try:
            if self.usar_pickle:
                with open(caminho, 'wb') as arquivo:
                    pickle.dump(combate, arquivo)
            else:
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    json.dump(combate.to_dict(), arquivo, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar combate: {e}")
            return False
    
    def carregar_combate(self, combate_id: str) -> Optional[Combate]:
        """
        Load a combat from file
        
        Args:
            combate_id: ID of the combat to load
            
        Returns:
            The loaded combat if found, None otherwise
        """
        caminho = self._obter_caminho_combate(combate_id)
        
        if not os.path.exists(caminho):
            return None
        
        try:
            if self.usar_pickle:
                with open(caminho, 'rb') as arquivo:
                    return pickle.load(arquivo)
            else:
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    data = json.load(arquivo)
                    # Load the characters first
                    personagem1 = self.carregar_personagem(data["personagem1"]["id"])
                    personagem2 = self.carregar_personagem(data["personagem2"]["id"])
                    
                    if not personagem1 or not personagem2:
                        return None
                    
                    # Create and configure the combat
                    return Combate.from_dict(data, personagem1, personagem2)
        except Exception as e:
            print(f"Erro ao carregar combate: {e}")
            return None
    
    def excluir_combate(self, combate_id: str) -> bool:
        """
        Delete a combat file
        
        Args:
            combate_id: ID of the combat to delete
            
        Returns:
            True if successful, False otherwise
        """
        caminho = self._obter_caminho_combate(combate_id)
        
        if not os.path.exists(caminho):
            return False
        
        try:
            os.remove(caminho)
            return True
        except Exception as e:
            print(f"Erro ao excluir combate: {e}")
            return False
    
    def salvar_historico_combate(self, combate: Combate) -> bool:
        """
        Save a combat to history
        
        Args:
            combate: Finished combat to save
            
        Returns:
            True if successful, False otherwise
        """
        if not combate.finalizado:
            return False
        
        caminho = self._obter_caminho_historico(combate.id)
        
        # Create a summary of the combat
        resumo = {
            "id": combate.id,
            "data": None,  # Would be datetime.now() in real implementation
            "personagem1": {
                "id": combate.personagem1.id,
                "nome": combate.personagem1.nome,
                "classe": combate.personagem1.classe
            },
            "personagem2": {
                "id": combate.personagem2.id,
                "nome": combate.personagem2.nome,
                "classe": combate.personagem2.classe
            },
            "vencedor": {
                "id": combate.vencedor.id,
                "nome": combate.vencedor.nome,
                "classe": combate.vencedor.classe
            } if combate.vencedor else None,
            "turnos": combate.turno_atual,
            "log": combate.log_combate
        }
        
        try:
            if self.usar_pickle:
                with open(caminho, 'wb') as arquivo:
                    pickle.dump(resumo, arquivo)
            else:
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    json.dump(resumo, arquivo, ensure_ascii=False, indent=2)
            
            # After saving to history, remove from active combats
            self.excluir_combate(combate.id)
            return True
        except Exception as e:
            print(f"Erro ao salvar histórico de combate: {e}")
            return False
    
    def carregar_historico_combates(self) -> List[Dict[str, Any]]:
        """
        Load all combat history
        
        Returns:
            List of all combat history entries
        """
        historico = []
        
        ext = ".pkl" if self.usar_pickle else ".json"
        for arquivo in os.listdir(self.historico_dir):
            if arquivo.endswith(ext):
                caminho = os.path.join(self.historico_dir, arquivo)
                
                try:
                    if self.usar_pickle:
                        with open(caminho, 'rb') as arquivo_hist:
                            historico.append(pickle.load(arquivo_hist))
                    else:
                        with open(caminho, 'r', encoding='utf-8') as arquivo_hist:
                            historico.append(json.load(arquivo_hist))
                except Exception as e:
                    print(f"Erro ao carregar histórico: {e}")
        
        # Sort by date (if implemented) or ID
        return historico