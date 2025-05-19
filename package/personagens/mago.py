"""
Mage character class for the Medieval Fantasy Battle Simulator.
Specializes in magical combat with high intelligence and spell variety.
"""

from typing import Dict, Any, Optional, List
from package.personagens.base import Personagem
from package.personagens.mixins import ElementalMixin


class Mago(Personagem, ElementalMixin):
    """
    Mage class that specializes in magical combat.
    Features high intelligence, spell variety, and elemental mastery.
    """
    
    def __init__(self, nome: str):
        """
        Initialize a new Mage character
        
        Args:
            nome: The mage's name
        """
        # Initialize base character
        super().__init__(nome)
        
        # Override base stats with mage specialization
        self.inteligencia += 5  # Extra intelligence
        self.forca -= 2         # Less physical strength
        self.vida_maxima -= 10  # Less health
        self.vida_atual = self.vida_maxima
        
        # Mage-specific attributes
        self.mana = 100
        self.mana_maxima = 100
        self.elemento_ativo = "fogo"  # Default element
        
        # Initialize elemental magic from mixin
        self.initialize_elemental("fogo")
        
        # Add mage-specific abilities
        self._habilidades = [
            {
                "id": "bola_de_fogo",
                "nome": "Bola de Fogo",
                "descricao": "Conjura uma bola de fogo que causa dano ao alvo",
                "custo": 25,  # Mana cost
                "tipo": "ataque",
                "elemento": "fogo",
                "multiplicador": 2.0
            },
            {
                "id": "raio_de_gelo",
                "nome": "Raio de Gelo",
                "descricao": "Conjura um raio de gelo que causa dano e reduz a velocidade do alvo",
                "custo": 30,
                "tipo": "ataque",
                "elemento": "gelo",
                "multiplicador": 1.6,
                "efeito": "lentidao"
            },
            {
                "id": "barreira_arcana",
                "nome": "Barreira Arcana",
                "descricao": "Cria uma barreira mágica que absorve dano",
                "custo": 35,
                "tipo": "defesa",
                "duracao": 2,  # Turns
                "absorve_dano": 40
            },
            {
                "id": "mudar_elemento",
                "nome": "Mudar Elemento",
                "descricao": "Muda o elemento ativo do mago",
                "custo": 10,
                "tipo": "utilidade",
                "elementos_disponiveis": ["fogo", "gelo", "raio", "arcano"]
            }
        ]
    
    def calcular_dano_ataque(self) -> int:
        """
        Calculate mage attack damage based on intelligence
        
        Returns:
            Calculated damage amount
        """
        # Base damage from intelligence
        dano_base = int(self.inteligencia * 1.2)
        
        # Add staff/wand damage if equipped
        if self._equipamentos["arma"]:
            dano_base += self._equipamentos["arma"].get("dano", 0)
        
        # Apply elemental bonus from current element
        dano_base = int(dano_base * self.elemental_damage_multiplier)
        
        return dano_base
    
    def defender(self, dano_recebido: int) -> int:
        """
        Calculate mage's damage reduction when defending
        
        Args:
            dano_recebido: The incoming damage
            
        Returns:
            Amount of damage reduced
        """
        # Mages get less physical defense but can use mana for defense
        reducao_base = super().defender(dano_recebido)
        
        # Use mana to enhance defense if available
        if self.mana >= 10:
            mana_usada = min(10, self.mana)
            self.gastar_mana(mana_usada)
            reducao_extra = int(mana_usada * 1.5)
            return reducao_base + reducao_extra
        
        return reducao_base
    
    def regenerar_mana(self, quantidade: int) -> int:
        """
        Regenerate mana
        
        Args:
            quantidade: Amount of mana to regenerate
            
        Returns:
            Current mana after regeneration
        """
        self.mana = min(self.mana_maxima, self.mana + quantidade)
        return self.mana
    
    def gastar_mana(self, quantidade: int) -> bool:
        """
        Spend mana resource
        
        Args:
            quantidade: Amount of mana to spend
            
        Returns:
            True if successful, False if not enough mana
        """
        if self.mana >= quantidade:
            self.mana -= quantidade
            return True
        return False
    
    def mudar_elemento(self, elemento: str) -> Dict[str, Any]:
        """
        Change active element
        
        Args:
            elemento: The element to switch to
            
        Returns:
            Result of the element change
        """
        if elemento in ["fogo", "gelo", "raio", "arcano"]:
            self.change_element(elemento)
            return {
                "sucesso": True,
                "elemento_anterior": self.elemento_ativo,
                "elemento_novo": elemento
            }
        return {
            "sucesso": False,
            "mensagem": "Elemento inválido"
        }
    
    def usar_habilidade(self, habilidade_id: str, alvo: Optional[Personagem] = None) -> Dict[str, Any]:
        """
        Use a mage ability
        
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
        
        # Check if we have enough mana
        if not self.gastar_mana(habilidade["custo"]):
            return {"sucesso": False, "mensagem": "Mana insuficiente"}
        
        resultado = {
            "sucesso": True,
            "tipo": "habilidade",
            "habilidade": habilidade["nome"],
            "usuario": self.nome,
        }
        
        # Handle ability effects based on type
        if habilidade["id"] in ["bola_de_fogo", "raio_de_gelo"] and alvo:
            # Set element temporarily if different from active
            old_element = self.elemento_ativo
            if "elemento" in habilidade and habilidade["elemento"] != self.elemento_ativo:
                self.mudar_elemento(habilidade["elemento"])
            
            # Calculate damage
            dano_base = self.calcular_dano_ataque()
            dano_final = int(dano_base * habilidade["multiplicador"])
            
            # Apply damage to target
            alvo.vida_atual = max(0, alvo.vida_atual - dano_final)
            
            # Apply additional effects
            efeitos = []
            if "efeito" in habilidade:
                if habilidade["efeito"] == "lentidao":
                    # Apply slow effect (would be handled by combat system)
                    efeitos.append("lentidao")
            
            # Restore original element if changed
            if "elemento" in habilidade and habilidade["elemento"] != old_element:
                self.mudar_elemento(old_element)
            
            resultado.update({
                "alvo": alvo.nome,
                "dano": dano_final,
                "vida_restante_alvo": alvo.vida_atual,
                "efeitos": efeitos
            })
            
        elif habilidade["id"] == "barreira_arcana":
            # Apply arcane barrier (would be handled by combat system)
            resultado.update({
                "barreira": habilidade["absorve_dano"],
                "duracao": habilidade["duracao"]
            })
            
        elif habilidade["id"] == "mudar_elemento":
            # Change active element based on user choice
            novo_elemento = "fogo"  # Default, would be chosen by user
            if alvo and isinstance(alvo, str) and alvo in habilidade["elementos_disponiveis"]:
                novo_elemento = alvo
            
            mudanca = self.mudar_elemento(novo_elemento)
            resultado.update(mudanca)
        
        return resultado
    
    def _aplicar_bonus_nivel(self) -> None:
        """Apply bonuses when leveling up (mage specialization)"""
        super()._aplicar_bonus_nivel()
        # Mages gain extra intelligence and mana on level up
        self.inteligencia += 2
        self.mana_maxima += 15
        self.mana = self.mana_maxima  # Restore mana on level up
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert mage to dictionary for serialization
        
        Returns:
            Dictionary representation of the mage
        """
        data = super().to_dict()
        # Add mage-specific properties
        data.update({
            "mana": self.mana,
            "mana_maxima": self.mana_maxima,
            "elemento_ativo": self.elemento_ativo,
            "elemental_damage_multiplier": self.elemental_damage_multiplier
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Mago':
        """
        Create mage from dictionary
        
        Args:
            data: Dictionary with mage data
            
        Returns:
            New mage instance
        """
        mago = cls(data["nome"])
        
        # Set basic properties
        for attr in ["id", "nivel", "experiencia", "vida_maxima", "vida_atual",
                    "forca", "destreza", "inteligencia", "constituicao"]:
            if attr in data:
                setattr(mago, attr, data[attr])
        
        # Set mage-specific properties
        if "mana" in data:
            mago.mana = data["mana"]
        if "mana_maxima" in data:
            mago.mana_maxima = data["mana_maxima"]
        
        # Set element if present
        if "elemento_ativo" in data:
            mago.mudar_elemento(data["elemento_ativo"])
        
        # Set collections
        if "habilidades" in data:
            mago._habilidades = data["habilidades"]
        if "inventario" in data:
            mago._inventario = data["inventario"]
        if "equipamentos" in data:
            mago._equipamentos = data["equipamentos"]
        
        return mago