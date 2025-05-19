"""
Mixin classes for adding special abilities to characters
in the Medieval Fantasy Battle Simulator.
"""

import random
from typing import Dict, Any, Optional


class PrecisionMixin:
    """
    Mixin for characters that can perform precision attacks
    with a chance of critical hits.
    """
    
    def initialize_precision(self) -> None:
        """Initialize precision attributes"""
        self.critical_hit_chance = 10.0  # Base 10% crit chance
        self.critical_damage_multiplier = 1.5  # 50% extra damage on crits
        self.last_attack_was_critical = False
    
    def roll_critical_hit(self) -> bool:
        """
        Roll for a critical hit
        
        Returns:
            True if critical hit, False otherwise
        """
        roll = random.randint(1, 100)
        self.last_attack_was_critical = roll <= self.critical_hit_chance
        return self.last_attack_was_critical
    
    def increase_critical_chance(self, amount: float) -> float:
        """
        Increase critical hit chance
        
        Args:
            amount: Percentage points to increase by
            
        Returns:
            New critical hit chance
        """
        self.critical_hit_chance += amount
        return self.critical_hit_chance
    
    def increase_critical_damage(self, amount: float) -> float:
        """
        Increase critical damage multiplier
        
        Args:
            amount: Amount to increase multiplier by
            
        Returns:
            New critical damage multiplier
        """
        self.critical_damage_multiplier += amount
        return self.critical_damage_multiplier


class BerserkMixin:
    """
    Mixin for characters that can enter a berserk state,
    trading defense for offense.
    """
    
    def initialize_berserk(self) -> None:
        """Initialize berserk attributes"""
        self.is_berserk = False
        self.berserk_damage_multiplier = 1.5  # 50% more damage
        self.berserk_defense_penalty = 0.3  # 30% less defense
    
    def enter_berserk(self) -> Dict[str, Any]:
        """
        Enter berserk state
        
        Returns:
            Result of entering berserk state
        """
        if not self.is_berserk:
            self.is_berserk = True
            return {
                "sucesso": True,
                "mensagem": f"{self.nome} entrou em estado de fúria!",
                "bonus_dano": f"+{int((self.berserk_damage_multiplier-1)*100)}%",
                "penalidade_defesa": f"-{int(self.berserk_defense_penalty*100)}%"
            }
        return {
            "sucesso": False,
            "mensagem": f"{self.nome} já está em estado de fúria!"
        }
    
    def exit_berserk(self) -> Dict[str, Any]:
        """
        Exit berserk state
        
        Returns:
            Result of exiting berserk state
        """
        if self.is_berserk:
            self.is_berserk = False
            return {
                "sucesso": True,
                "mensagem": f"{self.nome} saiu do estado de fúria."
            }
        return {
            "sucesso": False,
            "mensagem": f"{self.nome} não está em estado de fúria!"
        }


class ElementalMixin:
    """
    Mixin for characters that can use elemental magic
    with different effects based on the active element.
    """
    
    def initialize_elemental(self, elemento_inicial: str) -> None:
        """
        Initialize elemental attributes
        
        Args:
            elemento_inicial: Starting element
        """
        self.elemento_ativo = elemento_inicial
        self.elemental_damage_multiplier = 1.0
        self.elementos_bonus = {
            "fogo": 1.2,    # Fire: 20% more damage
            "gelo": 1.1,    # Ice: 10% more damage, has slow effect
            "raio": 1.15,   # Lightning: 15% more damage, has stun chance
            "arcano": 1.25  # Arcane: 25% more damage, no special effect
        }
    
    def change_element(self, novo_elemento: str) -> bool:
        """
        Change active element
        
        Args:
            novo_elemento: Element to switch to
            
        Returns:
            True if successful, False otherwise
        """
        if novo_elemento in self.elementos_bonus:
            self.elemento_ativo = novo_elemento
            self.elemental_damage_multiplier = self.elementos_bonus[novo_elemento]
            return True
        return False
    
    def get_element_effects(self) -> Dict[str, Any]:
        """
        Get effects of current element
        
        Returns:
            Dictionary with element effects
        """
        efeitos = {
            "elemento": self.elemento_ativo,
            "multiplicador_dano": self.elemental_damage_multiplier
        }
        
        # Add specific element effects
        if self.elemento_ativo == "fogo":
            efeitos["efeito_especial"] = "queimadura"
            efeitos["descricao"] = "Causa dano ao longo do tempo"
        elif self.elemento_ativo == "gelo":
            efeitos["efeito_especial"] = "lentidao"
            efeitos["descricao"] = "Reduz a velocidade de ataque do alvo"
        elif self.elemento_ativo == "raio":
            efeitos["efeito_especial"] = "atordoamento"
            efeitos["descricao"] = "Chance de atordoar o alvo por um turno"
        elif self.elemento_ativo == "arcano":
            efeitos["efeito_especial"] = "penetracao_magica"
            efeitos["descricao"] = "Ignora parte da resistência mágica do alvo"
        
        return efeitos


class StealthMixin:
    """
    Mixin for characters that can enter stealth,
    gaining bonuses to their next attack or action.
    """
    
    def initialize_stealth(self) -> None:
        """Initialize stealth attributes"""
        self.is_stealthed = False
        self.stealth_attack_bonus = 1.5  # 50% more damage from stealth
        self.stealth_detection_chance = 10  # 10% chance to be detected per turn
    
    def enter_stealth(self) -> Dict[str, Any]:
        """
        Enter stealth mode
        
        Returns:
            Result of entering stealth
        """
        if not self.is_stealthed:
            self.is_stealthed = True
            return {
                "sucesso": True,
                "mensagem": f"{self.nome} entrou em modo furtivo!",
                "bonus_proximo_ataque": f"+{int((self.stealth_attack_bonus-1)*100)}%"
            }
        return {
            "sucesso": False,
            "mensagem": f"{self.nome} já está em modo furtivo!"
        }
    
    def exit_stealth(self, discovered: bool = False) -> Dict[str, Any]:
        """
        Exit stealth mode
        
        Args:
            discovered: Whether stealth was broken by being discovered
            
        Returns:
            Result of exiting stealth
        """
        if self.is_stealthed:
            self.is_stealthed = False
            if discovered:
                return {
                    "sucesso": True,
                    "mensagem": f"{self.nome} foi descoberto e saiu do modo furtivo!"
                }
            return {
                "sucesso": True,
                "mensagem": f"{self.nome} saiu do modo furtivo."
            }
        return {
            "sucesso": False,
            "mensagem": f"{self.nome} não está em modo furtivo!"
        }
    
    def check_stealth_detection(self) -> bool:
        """
        Check if character is detected while in stealth
        
        Returns:
            True if detected, False otherwise
        """
        if not self.is_stealthed:
            return False
        
        roll = random.randint(1, 100)
        return roll <= self.stealth_detection_chance