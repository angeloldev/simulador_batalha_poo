"""
Abilities module for the Medieval Fantasy Battle Simulator.
Defines ability types, effects, and implementations.
"""

from typing import Dict, Any, List, Optional, Callable
import uuid


class Habilidade:
    """
    Base class for character abilities with different effects.
    """
    
    def __init__(self, nome: str, descricao: str, custo: int, tipo: str):
        """
        Initialize a new ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost (mana, stamina, etc.)
            tipo: Ability type (attack, defense, utility, etc.)
        """
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        self.custo = custo
        self.tipo = tipo
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert ability to dictionary
        
        Returns:
            Dictionary representation of the ability
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "custo": self.custo,
            "tipo": self.tipo
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Habilidade':
        """
        Create ability from dictionary
        
        Args:
            data: Dictionary with ability data
            
        Returns:
            New ability instance
        """
        habilidade = cls(
            data["nome"],
            data["descricao"],
            data["custo"],
            data["tipo"]
        )
        
        if "id" in data:
            habilidade.id = data["id"]
        
        return habilidade


class HabilidadeAtaque(Habilidade):
    """
    Attack ability that deals damage to a target.
    """
    
    def __init__(self, nome: str, descricao: str, custo: int, multiplicador: float, elemento: Optional[str] = None):
        """
        Initialize a new attack ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            multiplicador: Damage multiplier
            elemento: Optional elemental type
        """
        super().__init__(nome, descricao, custo, "ataque")
        self.multiplicador = multiplicador
        self.elemento = elemento
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert attack ability to dictionary
        
        Returns:
            Dictionary representation of the attack ability
        """
        data = super().to_dict()
        data.update({
            "multiplicador": self.multiplicador
        })
        
        if self.elemento:
            data["elemento"] = self.elemento
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HabilidadeAtaque':
        """
        Create attack ability from dictionary
        
        Args:
            data: Dictionary with ability data
            
        Returns:
            New attack ability instance
        """
        habilidade = cls(
            data["nome"],
            data["descricao"],
            data["custo"],
            data["multiplicador"],
            data.get("elemento")
        )
        
        if "id" in data:
            habilidade.id = data["id"]
        
        return habilidade


class HabilidadeDefesa(Habilidade):
    """
    Defense ability that reduces damage or provides protection.
    """
    
    def __init__(self, nome: str, descricao: str, custo: int, bonus_defesa: float, duracao: int):
        """
        Initialize a new defense ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            bonus_defesa: Defense bonus multiplier
            duracao: Duration in turns
        """
        super().__init__(nome, descricao, custo, "defesa")
        self.bonus_defesa = bonus_defesa
        self.duracao = duracao
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert defense ability to dictionary
        
        Returns:
            Dictionary representation of the defense ability
        """
        data = super().to_dict()
        data.update({
            "bonus_defesa": self.bonus_defesa,
            "duracao": self.duracao
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HabilidadeDefesa':
        """
        Create defense ability from dictionary
        
        Args:
            data: Dictionary with ability data
            
        Returns:
            New defense ability instance
        """
        habilidade = cls(
            data["nome"],
            data["descricao"],
            data["custo"],
            data["bonus_defesa"],
            data["duracao"]
        )
        
        if "id" in data:
            habilidade.id = data["id"]
        
        return habilidade


class HabilidadeUtilidade(Habilidade):
    """
    Utility ability that provides various non-combat effects.
    """
    
    def __init__(self, nome: str, descricao: str, custo: int, efeito: Callable[..., Dict[str, Any]]):
        """
        Initialize a new utility ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            efeito: Function that implements the ability effect
        """
        super().__init__(nome, descricao, custo, "utilidade")
        self.efeito = efeito
    
    def executar(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the ability effect
        
        Returns:
            Result of the ability effect
        """
        return self.efeito(*args, **kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert utility ability to dictionary
        
        Returns:
            Dictionary representation of the utility ability
        """
        data = super().to_dict()
        # Can't serialize the function, so we store the function name instead
        data["efeito_nome"] = self.efeito.__name__
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], efeitos_map: Dict[str, Callable]) -> 'HabilidadeUtilidade':
        """
        Create utility ability from dictionary
        
        Args:
            data: Dictionary with ability data
            efeitos_map: Mapping of effect names to functions
            
        Returns:
            New utility ability instance
        """
        if "efeito_nome" not in data or data["efeito_nome"] not in efeitos_map:
            raise ValueError("Effect not found for utility ability")
        
        habilidade = cls(
            data["nome"],
            data["descricao"],
            data["custo"],
            efeitos_map[data["efeito_nome"]]
        )
        
        if "id" in data:
            habilidade.id = data["id"]
        
        return habilidade


class GerenciadorHabilidades:
    """
    Manager for creating and tracking abilities.
    """
    
    def __init__(self):
        """Initialize a new ability manager"""
        self.habilidades = {}
        self.efeitos_map = {}
    
    def registrar_efeito(self, nome: str, funcao: Callable) -> None:
        """
        Register an effect function for utility abilities
        
        Args:
            nome: Effect name
            funcao: Effect function
        """
        self.efeitos_map[nome] = funcao
    
    def criar_habilidade_ataque(self, nome: str, descricao: str, custo: int, 
                               multiplicador: float, elemento: Optional[str] = None) -> HabilidadeAtaque:
        """
        Create and register a new attack ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            multiplicador: Damage multiplier
            elemento: Optional elemental type
            
        Returns:
            The created attack ability
        """
        habilidade = HabilidadeAtaque(nome, descricao, custo, multiplicador, elemento)
        self.habilidades[habilidade.id] = habilidade
        return habilidade
    
    def criar_habilidade_defesa(self, nome: str, descricao: str, custo: int,
                               bonus_defesa: float, duracao: int) -> HabilidadeDefesa:
        """
        Create and register a new defense ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            bonus_defesa: Defense bonus multiplier
            duracao: Duration in turns
            
        Returns:
            The created defense ability
        """
        habilidade = HabilidadeDefesa(nome, descricao, custo, bonus_defesa, duracao)
        self.habilidades[habilidade.id] = habilidade
        return habilidade
    
    def criar_habilidade_utilidade(self, nome: str, descricao: str, custo: int,
                                 efeito_nome: str) -> HabilidadeUtilidade:
        """
        Create and register a new utility ability
        
        Args:
            nome: Ability name
            descricao: Ability description
            custo: Resource cost
            efeito_nome: Name of registered effect
            
        Returns:
            The created utility ability
        """
        if efeito_nome not in self.efeitos_map:
            raise ValueError(f"Effect '{efeito_nome}' not registered")
        
        habilidade = HabilidadeUtilidade(nome, descricao, custo, self.efeitos_map[efeito_nome])
        self.habilidades[habilidade.id] = habilidade
        return habilidade
    
    def obter_habilidade(self, habilidade_id: str) -> Optional[Habilidade]:
        """
        Get an ability by ID
        
        Args:
            habilidade_id: ID of the ability
            
        Returns:
            The ability if found, None otherwise
        """
        return self.habilidades.get(habilidade_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert ability manager to dictionary
        
        Returns:
            Dictionary representation of the ability manager
        """
        return {
            "habilidades": {id: habilidade.to_dict() for id, habilidade in self.habilidades.items()}
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load abilities from dictionary
        
        Args:
            data: Dictionary with ability data
        """
        if "habilidades" in data:
            for id, habilidade_data in data["habilidades"].items():
                tipo = habilidade_data["tipo"]
                
                if tipo == "ataque":
                    habilidade = HabilidadeAtaque.from_dict(habilidade_data)
                elif tipo == "defesa":
                    habilidade = HabilidadeDefesa.from_dict(habilidade_data)
                elif tipo == "utilidade":
                    habilidade = HabilidadeUtilidade.from_dict(habilidade_data, self.efeitos_map)
                else:
                    habilidade = Habilidade.from_dict(habilidade_data)
                
                self.habilidades[id] = habilidade