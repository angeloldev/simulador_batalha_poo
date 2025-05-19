"""
Combat system module for the Medieval Fantasy Battle Simulator.
Handles battle mechanics, turns, and action resolution.
"""

import uuid
import random
from typing import Dict, Any, List, Optional, Union
from package.personagens.base import Personagem


class Combate:
    """
    Class that manages combat between two characters,
    handling turns, actions, and battle resolution.
    """
    
    def __init__(self, personagem1: Personagem, personagem2: Personagem):
        """
        Initialize a new combat session between two characters
        
        Args:
            personagem1: First character
            personagem2: Second character
        """
        self.id = str(uuid.uuid4())
        self.personagem1 = personagem1
        self.personagem2 = personagem2
        self.turno_atual = 1
        self.personagem_ativo = self._determinar_primeiro_personagem()
        self.finalizado = False
        self.vencedor = None
        self.log_combate = []
        
        # Reset characters to battle state
        self._resetar_personagens()
    
    def _resetar_personagens(self) -> None:
        """Reset characters to their battle state"""
        # Reset defense stance
        self.personagem1.set_estado_defesa(False)
        self.personagem2.set_estado_defesa(False)
        
        # Reset any combat-specific attributes
        # (would add more resets here for temporary combat effects)
    
    def _determinar_primeiro_personagem(self) -> Personagem:
        """
        Determine which character goes first based on attributes
        
        Returns:
            The character that goes first
        """
        # Base initiative on dexterity with some randomness
        iniciativa1 = self.personagem1.destreza + random.randint(1, 10)
        iniciativa2 = self.personagem2.destreza + random.randint(1, 10)
        
        if iniciativa1 >= iniciativa2:
            return self.personagem1
        return self.personagem2
    
    def _alternar_personagem_ativo(self) -> None:
        """Switch the active character for the next turn"""
        if self.personagem_ativo == self.personagem1:
            self.personagem_ativo = self.personagem2
        else:
            self.personagem_ativo = self.personagem1
            # Increment turn counter when both characters have acted
            self.turno_atual += 1
    
    def _verificar_fim_combate(self) -> bool:
        """
        Check if combat is over
        
        Returns:
            True if combat is over, False otherwise
        """
        if self.personagem1.vida_atual <= 0:
            self.finalizado = True
            self.vencedor = self.personagem2
            return True
        
        if self.personagem2.vida_atual <= 0:
            self.finalizado = True
            self.vencedor = self.personagem1
            return True
        
        return False
    
    def _obter_personagem_inativo(self) -> Personagem:
        """
        Get the non-active character
        
        Returns:
            The character that is not currently active
        """
        if self.personagem_ativo == self.personagem1:
            return self.personagem2
        return self.personagem1
    
    def executar_ataque(self) -> Dict[str, Any]:
        """
        Execute attack action for the active character
        
        Returns:
            Result of the attack action
        """
        if self.finalizado:
            return {"erro": "Combate já finalizado"}
        
        atacante = self.personagem_ativo
        defensor = self._obter_personagem_inativo()
        
        # Execute attack
        resultado = atacante.atacar(defensor)
        
        # Log the action
        log_entry = {
            "turno": self.turno_atual,
            "acao": "ataque",
            "atacante": atacante.nome,
            "defensor": defensor.nome,
            "dano": resultado["dano_final"],
            "vida_restante_defensor": defensor.vida_atual
        }
        self.log_combate.append(log_entry)
        
        # Check if combat is over
        self._verificar_fim_combate()
        
        # Switch active character
        self._alternar_personagem_ativo()
        
        return resultado
    
    def executar_defesa(self) -> Dict[str, Any]:
        """
        Execute defense action for the active character
        
        Returns:
            Result of the defense action
        """
        if self.finalizado:
            return {"erro": "Combate já finalizado"}
        
        defensor = self.personagem_ativo
        
        # Set defense stance
        defensor.set_estado_defesa(True)
        
        # Log the action
        log_entry = {
            "turno": self.turno_atual,
            "acao": "defesa",
            "personagem": defensor.nome
        }
        self.log_combate.append(log_entry)
        
        # Switch active character
        self._alternar_personagem_ativo()
        
        return {
            "tipo": "defesa",
            "personagem": defensor.nome,
            "mensagem": f"{defensor.nome} assume postura defensiva."
        }
    
    def usar_habilidade(self, habilidade_id: str) -> Dict[str, Any]:
        """
        Use an ability for the active character
        
        Args:
            habilidade_id: ID of the ability to use
            
        Returns:
            Result of the ability usage
        """
        if self.finalizado:
            return {"erro": "Combate já finalizado"}
        
        # Get characters
        usuario = self.personagem_ativo
        alvo = self._obter_personagem_inativo()
        
        # Use the ability
        resultado = usuario.usar_habilidade(habilidade_id, alvo)
        
        # Log the action
        log_entry = {
            "turno": self.turno_atual,
            "acao": "habilidade",
            "usuario": usuario.nome,
            "habilidade": resultado.get("habilidade", "desconhecida"),
            "resultado": resultado
        }
        self.log_combate.append(log_entry)
        
        # Check if combat is over
        self._verificar_fim_combate()
        
        # Switch active character
        self._alternar_personagem_ativo()
        
        return resultado
    
    def obter_resumo_combate(self) -> Dict[str, Any]:
        """
        Get a summary of the current combat state
        
        Returns:
            Summary of the combat
        """
        return {
            "id": self.id,
            "turno_atual": self.turno_atual,
            "personagem1": {
                "id": self.personagem1.id,
                "nome": self.personagem1.nome,
                "classe": self.personagem1.classe,
                "vida_atual": self.personagem1.vida_atual,
                "vida_maxima": self.personagem1.vida_maxima,
                "estado_defesa": self.personagem1.estado_defesa
            },
            "personagem2": {
                "id": self.personagem2.id,
                "nome": self.personagem2.nome,
                "classe": self.personagem2.classe,
                "vida_atual": self.personagem2.vida_atual,
                "vida_maxima": self.personagem2.vida_maxima,
                "estado_defesa": self.personagem2.estado_defesa
            },
            "personagem_ativo": self.personagem_ativo.id,
            "finalizado": self.finalizado,
            "vencedor": self.vencedor.nome if self.finalizado and self.vencedor else None,
            "num_acoes": len(self.log_combate)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert combat to dictionary for serialization
        
        Returns:
            Dictionary representation of the combat
        """
        return {
            "id": self.id,
            "personagem1": self.personagem1.to_dict(),
            "personagem2": self.personagem2.to_dict(),
            "turno_atual": self.turno_atual,
            "personagem_ativo": self.personagem_ativo.id,
            "finalizado": self.finalizado,
            "vencedor": self.vencedor.id if self.finalizado and self.vencedor else None,
            "log_combate": self.log_combate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], personagem1: Personagem, personagem2: Personagem) -> 'Combate':
        """
        Create combat from dictionary
        
        Args:
            data: Dictionary with combat data
            personagem1: First character
            personagem2: Second character
            
        Returns:
            New combat instance
        """
        combate = cls(personagem1, personagem2)
        
        # Set basic properties
        if "id" in data:
            combate.id = data["id"]
        if "turno_atual" in data:
            combate.turno_atual = data["turno_atual"]
        if "finalizado" in data:
            combate.finalizado = data["finalizado"]
        if "log_combate" in data:
            combate.log_combate = data["log_combate"]
        
        # Set active character
        if "personagem_ativo" in data:
            if data["personagem_ativo"] == personagem1.id:
                combate.personagem_ativo = personagem1
            else:
                combate.personagem_ativo = personagem2
        
        # Set winner if combat is finished
        if combate.finalizado and "vencedor" in data:
            if data["vencedor"] == personagem1.id:
                combate.vencedor = personagem1
            elif data["vencedor"] == personagem2.id:
                combate.vencedor = personagem2
        
        return combate