"""
Archer character class for the Medieval Fantasy Battle Simulator.
Specializes in ranged combat with high dexterity and critical strikes.
"""

from typing import Dict, Any, Optional, List
from package.personagens.base import Personagem
from package.personagens.mixins import PrecisionMixin


class Arqueiro(Personagem, PrecisionMixin):
    """
    Archer class that specializes in ranged combat.
    Features high dexterity, critical strikes, and precision attacks.
    """
    
    def __init__(self, nome: str):
        """
        Initialize a new Archer character
        
        Args:
            nome: The archer's name
        """
        # Initialize base character
        super().__init__(nome)
        
        # Override base stats with archer specialization
        self.destreza += 5       # Extra dexterity
        self.constituicao -= 1   # Less constitution
        self.vida_maxima -= 5    # Less health
        self.vida_atual = self.vida_maxima
        
        # Archer-specific attributes
        self.stamina = 100
        self.stamina_maxima = 100
        self.municao = 20        # Arrows
        self.flechas_especiais = []
        
        # Initialize precision system from mixin
        self.initialize_precision()
        
        # Add archer-specific abilities
        self._habilidades = [
            {
                "id": "tiro_certeiro",
                "nome": "Tiro Certeiro",
                "descricao": "Um tiro preciso que causa dano extra",
                "custo": 25,  # Stamina cost
                "tipo": "ataque",
                "multiplicador": 1.8,
                "bonus_critico": 15  # +15% crit chance
            },
            {
                "id": "chuva_de_flechas",
                "nome": "Chuva de Flechas",
                "descricao": "Dispara múltiplas flechas que causam dano em área",
                "custo": 40,
                "tipo": "ataque",
                "multiplicador": 1.2,
                "num_flechas": 3,
                "custo_municao": 3
            },
            {
                "id": "flecha_perfurante",
                "nome": "Flecha Perfurante",
                "descricao": "Uma flecha que ignora parte da defesa do alvo",
                "custo": 30,
                "tipo": "ataque",
                "multiplicador": 1.5,
                "penetracao_armadura": 0.3,  # Ignores 30% of armor
                "custo_municao": 1
            },
            {
                "id": "evasao",
                "nome": "Evasão",
                "descricao": "Aumenta a chance de esquivar de ataques",
                "custo": 20,
                "tipo": "defesa",
                "bonus_evasao": 0.3,  # +30% evasion
                "duracao": 2  # turns
            }
        ]
    
    def calcular_dano_ataque(self) -> int:
        """
        Calculate archer attack damage based on dexterity
        
        Returns:
            Calculated damage amount
        """
        # Base damage from dexterity
        dano_base = int(self.destreza * 1.3)
        
        # Add bow/weapon damage if equipped
        if self._equipamentos["arma"]:
            dano_base += self._equipamentos["arma"].get("dano", 0)
        
        # Check for critical hit
        if self.roll_critical_hit():
            dano_base = int(dano_base * self.critical_damage_multiplier)
        
        # Check ammunition
        if self.municao <= 0:
            dano_base = int(dano_base * 0.5)  # Reduced damage without arrows
        else:
            self.municao -= 1
        
        return dano_base
    
    def defender(self, dano_recebido: int) -> int:
        """
        Calculate archer's damage reduction when defending
        
        Args:
            dano_recebido: The incoming damage
            
        Returns:
            Amount of damage reduced
        """
        # Archers focus on evasion rather than damage reduction
        reducao_base = super().defender(dano_recebido)
        
        # Use stamina for better evasion if available
        if self.stamina >= 10:
            self.gastar_stamina(10)
            # Extra dodge chance (would be implemented in combat system)
            return reducao_base + int(self.destreza * 0.3)
        
        return reducao_base
    
    def regenerar_stamina(self, quantidade: int) -> int:
        """
        Regenerate stamina
        
        Args:
            quantidade: Amount of stamina to regenerate
            
        Returns:
            Current stamina after regeneration
        """
        self.stamina = min(self.stamina_maxima, self.stamina + quantidade)
        return self.stamina
    
    def gastar_stamina(self, quantidade: int) -> bool:
        """
        Spend stamina resource
        
        Args:
            quantidade: Amount of stamina to spend
            
        Returns:
            True if successful, False if not enough stamina
        """
        if self.stamina >= quantidade:
            self.stamina -= quantidade
            return True
        return False
    
    def adicionar_municao(self, quantidade: int) -> int:
        """
        Add ammunition (arrows)
        
        Args:
            quantidade: Number of arrows to add
            
        Returns:
            Current arrow count
        """
        self.municao += quantidade
        return self.municao
    
    def adicionar_flecha_especial(self, flecha: Dict[str, Any]) -> None:
        """
        Add a special arrow to inventory
        
        Args:
            flecha: Special arrow data
        """
        self.flechas_especiais.append(flecha)
    
    def usar_flecha_especial(self, flecha_id: str) -> Optional[Dict[str, Any]]:
        """
        Use a special arrow from inventory
        
        Args:
            flecha_id: ID of the special arrow
            
        Returns:
            The arrow if found, None otherwise
        """
        for i, flecha in enumerate(self.flechas_especiais):
            if flecha["id"] == flecha_id:
                return self.flechas_especiais.pop(i)
        return None
    
    def usar_habilidade(self, habilidade_id: str, alvo: Optional[Personagem] = None) -> Dict[str, Any]:
        """
        Use an archer ability
        
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
        
        # Check if we have enough stamina
        if not self.gastar_stamina(habilidade["custo"]):
            return {"sucesso": False, "mensagem": "Stamina insuficiente"}
        
        # Check ammunition for abilities that need it
        if "custo_municao" in habilidade:
            if self.municao < habilidade["custo_municao"]:
                # Refund stamina
                self.regenerar_stamina(habilidade["custo"])
                return {"sucesso": False, "mensagem": "Munição insuficiente"}
            self.municao -= habilidade["custo_municao"]
        
        resultado = {
            "sucesso": True,
            "tipo": "habilidade",
            "habilidade": habilidade["nome"],
            "usuario": self.nome,
        }
        
        # Handle ability effects based on type
        if habilidade["id"] == "tiro_certeiro" and alvo:
            # Temporarily increase crit chance
            old_crit_chance = self.critical_hit_chance
            self.critical_hit_chance += habilidade["bonus_critico"]
            
            # Calculate damage
            dano_base = self.calcular_dano_ataque()
            dano_final = int(dano_base * habilidade["multiplicador"])
            
            # Apply damage to target
            alvo.vida_atual = max(0, alvo.vida_atual - dano_final)
            
            # Reset crit chance
            self.critical_hit_chance = old_crit_chance
            
            resultado.update({
                "alvo": alvo.nome,
                "dano": dano_final,
                "vida_restante_alvo": alvo.vida_atual,
                "critico": self.last_attack_was_critical
            })
            
        elif habilidade["id"] == "chuva_de_flechas" and alvo:
            # Multiple attack simulation
            dano_total = 0
            for i in range(habilidade["num_flechas"]):
                dano_flecha = int(self.calcular_dano_ataque() * habilidade["multiplicador"])
                dano_total += dano_flecha
            
            # Apply damage to target
            alvo.vida_atual = max(0, alvo.vida_atual - dano_total)
            
            resultado.update({
                "alvo": alvo.nome,
                "num_flechas": habilidade["num_flechas"],
                "dano_total": dano_total,
                "vida_restante_alvo": alvo.vida_atual
            })
            
        elif habilidade["id"] == "flecha_perfurante" and alvo:
            # Calculate damage with armor penetration
            dano_base = self.calcular_dano_ataque()
            dano_final = int(dano_base * habilidade["multiplicador"])
            
            # Note: In real combat system, this would bypass a percentage of target's armor
            
            # Apply damage to target
            alvo.vida_atual = max(0, alvo.vida_atual - dano_final)
            
            resultado.update({
                "alvo": alvo.nome,
                "dano": dano_final,
                "penetracao_armadura": f"{int(habilidade['penetracao_armadura']*100)}%",
                "vida_restante_alvo": alvo.vida_atual
            })
            
        elif habilidade["id"] == "evasao":
            # Apply evasion bonus (would be handled by combat system)
            resultado.update({
                "bonus_evasao": f"{int(habilidade['bonus_evasao']*100)}%",
                "duracao": habilidade["duracao"]
            })
        
        return resultado
    
    def _aplicar_bonus_nivel(self) -> None:
        """Apply bonuses when leveling up (archer specialization)"""
        super()._aplicar_bonus_nivel()
        # Archers gain extra dexterity and critical chance on level up
        self.destreza += 2
        self.increase_critical_chance(1)  # +1% crit chance per level
        self.stamina_maxima += 10
        self.stamina = self.stamina_maxima  # Restore stamina on level up
        self.municao += 5  # Get some arrows on level up
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert archer to dictionary for serialization
        
        Returns:
            Dictionary representation of the archer
        """
        data = super().to_dict()
        # Add archer-specific properties
        data.update({
            "stamina": self.stamina,
            "stamina_maxima": self.stamina_maxima,
            "municao": self.municao,
            "flechas_especiais": self.flechas_especiais,
            "critical_hit_chance": self.critical_hit_chance,
            "critical_damage_multiplier": self.critical_damage_multiplier,
            "last_attack_was_critical": self.last_attack_was_critical
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Arqueiro':
        """
        Create archer from dictionary
        
        Args:
            data: Dictionary with archer data
            
        Returns:
            New archer instance
        """
        arqueiro = cls(data["nome"])
        
        # Set basic properties
        for attr in ["id", "nivel", "experiencia", "vida_maxima", "vida_atual",
                    "forca", "destreza", "inteligencia", "constituicao"]:
            if attr in data:
                setattr(arqueiro, attr, data[attr])
        
        # Set archer-specific properties
        if "stamina" in data:
            arqueiro.stamina = data["stamina"]
        if "stamina_maxima" in data:
            arqueiro.stamina_maxima = data["stamina_maxima"]
        if "municao" in data:
            arqueiro.municao = data["municao"]
        if "flechas_especiais" in data:
            arqueiro.flechas_especiais = data["flechas_especiais"]
        
        # Set precision attributes
        if "critical_hit_chance" in data:
            arqueiro.critical_hit_chance = data["critical_hit_chance"]
        if "critical_damage_multiplier" in data:
            arqueiro.critical_damage_multiplier = data["critical_damage_multiplier"]
        
        # Set collections
        if "habilidades" in data:
            arqueiro._habilidades = data["habilidades"]
        if "inventario" in data:
            arqueiro._inventario = data["inventario"]
        if "equipamentos" in data:
            arqueiro._equipamentos = data["equipamentos"]
        
        return arqueiro