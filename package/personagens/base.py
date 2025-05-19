"""
Base character module for the Medieval Fantasy Battle Simulator
Defines the abstract Personagem (Character) base class
"""

from abc import ABC, abstractmethod
import uuid
from typing import List, Dict, Any, Optional


class Personagem(ABC):
    """
    Abstract base class for all character types in the battle simulator.
    Implements base attributes and methods common to all characters.
    """
    
    def __init__(self, nome: str):
        """
        Initialize a new character with base attributes
        
        Args:
            nome: The character's name
        """
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = 1
        self.experiencia = 0
        self.vida_maxima = 100
        self.vida_atual = 100
        self.forca = 10
        self.destreza = 10
        self.inteligencia = 10
        self.constituicao = 10
        
        # Protected attributes - accessible to subclasses
        self._habilidades = []
        self._inventario = []
        self._equipamentos = {
            "arma": None,
            "armadura": None,
            "acessorio": None
        }
        
        # Private attributes - internal use only
        self.__classe = self.__class__.__name__
        self.__estado_defesa = False
    
    @property
    def classe(self) -> str:
        """Get the character's class name"""
        return self.__classe
    
    @property
    def habilidades(self) -> List[Dict[str, Any]]:
        """Get the character's abilities list"""
        return self._habilidades
    
    @property
    def inventario(self) -> List[Dict[str, Any]]:
        """Get the character's inventory"""
        return self._inventario
    
    @property
    def equipamentos(self) -> Dict[str, Any]:
        """Get the character's equipped items"""
        return self._equipamentos
    
    @property
    def estado_defesa(self) -> bool:
        """Check if character is in defense stance"""
        return self.__estado_defesa
    
    def set_estado_defesa(self, estado: bool) -> None:
        """Set the defense state"""
        self.__estado_defesa = estado
    
    def adicionar_habilidade(self, habilidade: Dict[str, Any]) -> None:
        """Add a new ability to the character"""
        self._habilidades.append(habilidade)
    
    def adicionar_item(self, item: Dict[str, Any]) -> None:
        """Add an item to the character's inventory"""
        self._inventario.append(item)
    
    def remover_item(self, item_id: str) -> bool:
        """Remove an item from inventory by id"""
        for i, item in enumerate(self._inventario):
            if item["id"] == item_id:
                self._inventario.pop(i)
                return True
        return False
    
    def equipar_item(self, item_id: str) -> bool:
        """Equip an item from inventory"""
        for item in self._inventario:
            if item["id"] == item_id:
                slot = item["tipo"]
                if slot in self._equipamentos:
                    # Unequip current item if any
                    if self._equipamentos[slot]:
                        self.desequipar_item(self._equipamentos[slot]["id"])
                    
                    # Equip new item
                    self._equipamentos[slot] = item
                    self._aplicar_bonus_equipamento(item)
                    return True
        return False
    
    def desequipar_item(self, item_id: str) -> bool:
        """Unequip an item by id"""
        for slot, item in self._equipamentos.items():
            if item and item["id"] == item_id:
                self._remover_bonus_equipamento(item)
                self._equipamentos[slot] = None
                return True
        return False
    
    def _aplicar_bonus_equipamento(self, item: Dict[str, Any]) -> None:
        """Apply equipment bonuses to character stats"""
        if "bonus" in item:
            for atributo, valor in item["bonus"].items():
                if hasattr(self, atributo):
                    setattr(self, atributo, getattr(self, atributo) + valor)
    
    def _remover_bonus_equipamento(self, item: Dict[str, Any]) -> None:
        """Remove equipment bonuses from character stats"""
        if "bonus" in item:
            for atributo, valor in item["bonus"].items():
                if hasattr(self, atributo):
                    setattr(self, atributo, getattr(self, atributo) - valor)
    
    def atacar(self, alvo: 'Personagem') -> Dict[str, Any]:
        """
        Execute a basic attack against a target
        
        Args:
            alvo: The target character to attack
            
        Returns:
            Dictionary with attack results
        """
        dano_base = self.calcular_dano_ataque()
        
        # Check if target is defending
        if alvo.estado_defesa:
            dano_reduzido = alvo.defender(dano_base)
            dano_final = dano_base - dano_reduzido
        else:
            dano_final = dano_base
        
        # Apply damage
        dano_final = max(1, dano_final)  # Minimum 1 damage
        alvo.vida_atual = max(0, alvo.vida_atual - dano_final)
        
        return {
            "tipo": "ataque",
            "atacante": self.nome,
            "alvo": alvo.nome,
            "dano_base": dano_base,
            "dano_final": dano_final,
            "vida_restante_alvo": alvo.vida_atual
        }
    
    def defender(self, dano_recebido: int) -> int:
        """
        Calculate damage reduction when defending
        
        Args:
            dano_recebido: The incoming damage
            
        Returns:
            Amount of damage reduced
        """
        # Base defense reduces 30% of damage
        reducao = int(dano_recebido * 0.3)
        self.set_estado_defesa(False)  # Defense stance lasts only one turn
        return reducao
    
    @abstractmethod
    def calcular_dano_ataque(self) -> int:
        """
        Calculate attack damage based on character attributes
        Must be implemented by subclasses
        
        Returns:
            The calculated damage amount
        """
        pass
    
    @abstractmethod
    def usar_habilidade(self, habilidade_id: str, alvo: Optional['Personagem'] = None) -> Dict[str, Any]:
        """
        Use a special ability
        Must be implemented by subclasses
        
        Args:
            habilidade_id: ID of the ability to use
            alvo: Optional target character
            
        Returns:
            Dictionary with ability usage results
        """
        pass
    
    def ganhar_experiencia(self, quantidade: int) -> Dict[str, Any]:
        """
        Gain experience points and level up if needed
        
        Args:
            quantidade: Amount of experience to gain
            
        Returns:
            Dictionary with experience gain results
        """
        self.experiencia += quantidade
        resultado = {
            "experiencia_ganha": quantidade,
            "experiencia_total": self.experiencia,
            "nivel_anterior": self.nivel,
            "subiu_nivel": False
        }
        
        # Check for level up (simple formula: 100 * current level)
        experiencia_proxima_nivel = 100 * self.nivel
        if self.experiencia >= experiencia_proxima_nivel:
            self.nivel += 1
            self.experiencia -= experiencia_proxima_nivel
            self._aplicar_bonus_nivel()
            resultado["subiu_nivel"] = True
            resultado["nivel_novo"] = self.nivel
        
        return resultado
    
    def _aplicar_bonus_nivel(self) -> None:
        """Apply bonuses when leveling up"""
        # Base level up bonuses
        self.vida_maxima += 10
        self.vida_atual = self.vida_maxima  # Heal on level up
        self.forca += 2
        self.destreza += 2
        self.inteligencia += 2
        self.constituicao += 2
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert character to dictionary for serialization
        
        Returns:
            Dictionary representation of the character
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "classe": self.classe,
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "vida_maxima": self.vida_maxima,
            "vida_atual": self.vida_atual,
            "forca": self.forca,
            "destreza": self.destreza,
            "inteligencia": self.inteligencia,
            "constituicao": self.constituicao,
            "habilidades": self._habilidades,
            "inventario": self._inventario,
            "equipamentos": self._equipamentos,
            "estado_defesa": self.estado_defesa
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Personagem':
        """
        Create character from dictionary (abstract factory method)
        Must be implemented by subclasses
        
        Args:
            data: Dictionary with character data
            
        Returns:
            New character instance
        """
        raise NotImplementedError("Must be implemented by subclasses")