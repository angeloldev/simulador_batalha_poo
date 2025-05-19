"""
Warrior character class for the Medieval Fantasy Battle Simulator.
Specializes in physical combat with high strength and defense.
"""

from typing import Dict, Any, Optional, List
from package.personagens.base import Personagem
from package.personagens.mixins import BerserkMixin


class Guerreiro(Personagem, BerserkMixin):
    """
    Warrior class that specializes in physical combat.
    Features high strength, constitution, and melee attack power.
    """
    
    def __init__(self, nome: str):
        """
        Initialize a new Warrior character
        
        Args:
            nome: The warrior's name
        """
        # Initialize base character
        super().__init__(nome)
        
        # Override base stats with warrior specialization
        self.forca += 5        # Extra strength
        self.constituicao += 3 # Extra health/toughness
        self.vida_maxima += 20 # More health
        self.vida_atual = self.vida_maxima
        
        # Warrior-specific attributes
        self.furia = 0         # Rage resource for special abilities
        self.furia_maxima = 100
        
        # Add warrior-specific abilities
        self._habilidades = [
            {
                "id": "golpe_poderoso",
                "nome": "Golpe Poderoso",
                "descricao": "Um golpe devastador que causa dano extra",
                "custo": 30,  # Fury cost
                "tipo": "ataque",
                "multiplicador": 1.5
            },
            {
                "id": "provocar",
                "nome": "Provocar",
                "descricao": "Provoca o inimigo, ganhando furia",
                "custo": 0,
                "tipo": "utilidade",
                "bonus_furia": 40
            },
            {
                "id": "postura_defensiva",
                "nome": "Postura Defensiva",
                "descricao": "Aumenta a defesa por um turno",
                "custo": 20,
                "tipo": "defesa",
                "bonus_defesa": 0.2  # 20% extra defense
            }
        ]
        
        # Initialize berserk state from mixin
        self.initialize_berserk()
    
    def calcular_dano_ataque(self) -> int:
        """
        Calculate warrior attack damage based on strength
        
        Returns:
            Calculated damage amount
        """
        dano_base = int(self.forca * 1.5)
        
        # Add weapon damage if equipped
        if self._equipamentos["arma"]:
            dano_base += self._equipamentos["arma"].get("dano", 0)
        
        # Add berserk bonus if active
        if self.is_berserk:
            dano_base = int(dano_base * self.berserk_damage_multiplier)
        
        # Generate fury on attack
        self.ganhar_furia(10)
        
        return dano_base
    
    def defender(self, dano_recebido: int) -> int:
        """
        Calculate warrior's damage reduction when defending
        
        Args:
            dano_recebido: The incoming damage
            
        Returns:
            Amount of damage reduced
        """
        # Warriors get extra defense from constitution
        reducao_base = super().defender(dano_recebido)
        reducao_extra = int(self.constituicao * 0.5)
        
        # Generate fury when taking damage
        self.ganhar_furia(15)
        
        return reducao_base + reducao_extra
    
    def ganhar_furia(self, quantidade: int) -> int:
        """
        Gain fury resource
        
        Args:
            quantidade: Amount of fury to gain
            
        Returns:
            Current fury after gain
        """
        self.furia = min(self.furia_maxima, self.furia + quantidade)
        
        # Check if berserk should activate
        if self.furia >= 80 and not self.is_berserk:
            self.enter_berserk()
        
        return self.furia
    
    def gastar_furia(self, quantidade: int) -> bool:
        """
        Spend fury resource
        
        Args:
            quantidade: Amount of fury to spend
            
        Returns:
            True if successful, False if not enough fury
        """
        if self.furia >= quantidade:
            self.furia -= quantidade
            
            # Check if berserk should deactivate
            if self.furia < 50 and self.is_berserk:
                self.exit_berserk()
                
            return True
        return False
    
    def usar_habilidade(self, habilidade_id: str, alvo: Optional[Personagem] = None) -> Dict[str, Any]:
        """
        Use a warrior ability
        
        Args:
            habilidade_id: ID of the ability to use
            alvo: Optional target character
            
        Returns:
            Dictionary with ability usage results
        """
        # Find the ability
        habilidade = next((h for h in self._habilidades if h["id"] == habilidade_id), None)
        if not habilidade:
            return {"sucesso": False, "mensagem": "Habilidade não encontrada"}
        
        # Check if we have enough fury
        if not self.gastar_furia(habilidade["custo"]):
            return {"sucesso": False, "mensagem": "Fúria insuficiente"}
        
        resultado = {
            "sucesso": True,
            "tipo": "habilidade",
            "habilidade": habilidade["nome"],
            "usuario": self.nome,
        }
        
        # Handle ability effects based on type
        if habilidade["id"] == "golpe_poderoso" and alvo:
            # Calculate damage
            dano_base = self.calcular_dano_ataque()
            dano_final = int(dano_base * habilidade["multiplicador"])
            
            # Apply damage to target
            alvo.vida_atual = max(0, alvo.vida_atual - dano_final)
            
            resultado.update({
                "alvo": alvo.nome,
                "dano": dano_final,
                "vida_restante_alvo": alvo.vida_atual
            })
            
        elif habilidade["id"] == "provocar":
            # Gain fury
            fury_gained = habilidade["bonus_furia"]
            self.ganhar_furia(fury_gained)
            
            resultado.update({
                "bonus_furia": fury_gained,
                "furia_atual": self.furia
            })
            
        elif habilidade["id"] == "postura_defensiva":
            # Set defense stance with bonus
            self.set_estado_defesa(True)
            
            resultado.update({
                "bonus_defesa": f"{int(habilidade['bonus_defesa']*100)}%",
                "duracao": "1 turno"
            })
        
        return resultado
    
    def _aplicar_bonus_nivel(self) -> None:
        """Apply bonuses when leveling up (warrior specialization)"""
        super()._aplicar_bonus_nivel()
        # Warriors gain extra strength and constitution on level up
        self.forca += 1
        self.constituicao += 1
        self.furia_maxima += 5
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert warrior to dictionary for serialization
        
        Returns:
            Dictionary representation of the warrior
        """
        data = super().to_dict()
        # Add warrior-specific properties
        data.update({
            "furia": self.furia,
            "furia_maxima": self.furia_maxima,
            "is_berserk": self.is_berserk,
            "berserk_damage_multiplier": self.berserk_damage_multiplier,
            "berserk_defense_penalty": self.berserk_defense_penalty
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Guerreiro':
        """
        Create warrior from dictionary
        
        Args:
            data: Dictionary with warrior data
            
        Returns:
            New warrior instance
        """
        guerreiro = cls(data["nome"])
        
        # Set basic properties
        for attr in ["id", "nivel", "experiencia", "vida_maxima", "vida_atual",
                    "forca", "destreza", "inteligencia", "constituicao"]:
            if attr in data:
                setattr(guerreiro, attr, data[attr])
        
        # Set warrior-specific properties
        if "furia" in data:
            guerreiro.furia = data["furia"]
        if "furia_maxima" in data:
            guerreiro.furia_maxima = data["furia_maxima"]
        
        # Set collections
        if "habilidades" in data:
            guerreiro._habilidades = data["habilidades"]
        if "inventario" in data:
            guerreiro._inventario = data["inventario"]
        if "equipamentos" in data:
            guerreiro._equipamentos = data["equipamentos"]
        
        # Set berserk state if needed
        if data.get("is_berserk", False):
            guerreiro.enter_berserk()
        
        return guerreiro