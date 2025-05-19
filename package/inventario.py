"""
Inventory module for the Medieval Fantasy Battle Simulator.
Defines item types, effects, and inventory management.
"""

from typing import Dict, Any, List, Optional
import uuid


class Item:
    """
    Base class for all items in the game.
    """
    
    def __init__(self, nome: str, descricao: str, tipo: str, valor: int = 0):
        """
        Initialize a new item
        
        Args:
            nome: Item name
            descricao: Item description
            tipo: Item type (weapon, armor, potion, etc.)
            valor: Item value in gold
        """
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert item to dictionary
        
        Returns:
            Dictionary representation of the item
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "valor": self.valor
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """
        Create item from dictionary
        
        Args:
            data: Dictionary with item data
            
        Returns:
            New item instance
        """
        item = cls(
            data["nome"],
            data["descricao"],
            data["tipo"],
            data.get("valor", 0)
        )
        
        if "id" in data:
            item.id = data["id"]
        
        return item


class Arma(Item):
    """
    Weapon item that can be equipped by characters.
    """
    
    def __init__(self, nome: str, descricao: str, dano: int, atributo: str, 
                duas_maos: bool = False, valor: int = 0):
        """
        Initialize a new weapon
        
        Args:
            nome: Weapon name
            descricao: Weapon description
            dano: Base damage value
            atributo: Primary attribute (strength, dexterity, intelligence)
            duas_maos: Whether it requires two hands
            valor: Weapon value in gold
        """
        super().__init__(nome, descricao, "arma", valor)
        self.dano = dano
        self.atributo = atributo
        self.duas_maos = duas_maos
        
        # Optional bonuses
        self.bonus = {}
    
    def adicionar_bonus(self, atributo: str, valor: int) -> None:
        """
        Add a stat bonus to the weapon
        
        Args:
            atributo: The attribute to boost
            valor: Bonus amount
        """
        self.bonus[atributo] = valor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert weapon to dictionary
        
        Returns:
            Dictionary representation of the weapon
        """
        data = super().to_dict()
        data.update({
            "dano": self.dano,
            "atributo": self.atributo,
            "duas_maos": self.duas_maos,
            "bonus": self.bonus
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Arma':
        """
        Create weapon from dictionary
        
        Args:
            data: Dictionary with weapon data
            
        Returns:
            New weapon instance
        """
        arma = cls(
            data["nome"],
            data["descricao"],
            data["dano"],
            data["atributo"],
            data.get("duas_maos", False),
            data.get("valor", 0)
        )
        
        if "id" in data:
            arma.id = data["id"]
        
        if "bonus" in data:
            arma.bonus = data["bonus"]
        
        return arma


class Armadura(Item):
    """
    Armor item that can be equipped by characters.
    """
    
    def __init__(self, nome: str, descricao: str, defesa: int, 
                tipo_armadura: str, requisito_forca: int = 0, valor: int = 0):
        """
        Initialize a new armor
        
        Args:
            nome: Armor name
            descricao: Armor description
            defesa: Defense value
            tipo_armadura: Armor type (light, medium, heavy)
            requisito_forca: Required strength to equip
            valor: Armor value in gold
        """
        super().__init__(nome, descricao, "armadura", valor)
        self.defesa = defesa
        self.tipo_armadura = tipo_armadura
        self.requisito_forca = requisito_forca
        
        # Optional bonuses
        self.bonus = {}
        self.penalidades = {}
    
    def adicionar_bonus(self, atributo: str, valor: int) -> None:
        """
        Add a stat bonus to the armor
        
        Args:
            atributo: The attribute to boost
            valor: Bonus amount
        """
        self.bonus[atributo] = valor
    
    def adicionar_penalidade(self, atributo: str, valor: int) -> None:
        """
        Add a stat penalty to the armor
        
        Args:
            atributo: The attribute to penalize
            valor: Penalty amount (negative)
        """
        self.penalidades[atributo] = valor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert armor to dictionary
        
        Returns:
            Dictionary representation of the armor
        """
        data = super().to_dict()
        data.update({
            "defesa": self.defesa,
            "tipo_armadura": self.tipo_armadura,
            "requisito_forca": self.requisito_forca,
            "bonus": self.bonus,
            "penalidades": self.penalidades
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Armadura':
        """
        Create armor from dictionary
        
        Args:
            data: Dictionary with armor data
            
        Returns:
            New armor instance
        """
        armadura = cls(
            data["nome"],
            data["descricao"],
            data["defesa"],
            data["tipo_armadura"],
            data.get("requisito_forca", 0),
            data.get("valor", 0)
        )
        
        if "id" in data:
            armadura.id = data["id"]
        
        if "bonus" in data:
            armadura.bonus = data["bonus"]
        
        if "penalidades" in data:
            armadura.penalidades = data["penalidades"]
        
        return armadura


class Consumivel(Item):
    """
    Consumable item that can be used by characters.
    """
    
    def __init__(self, nome: str, descricao: str, efeito: Dict[str, Any], duracao: int = 0, valor: int = 0):
        """
        Initialize a new consumable
        
        Args:
            nome: Consumable name
            descricao: Consumable description
            efeito: Effect when used
            duracao: Duration of effect in turns (0 for instant)
            valor: Consumable value in gold
        """
        super().__init__(nome, descricao, "consumivel", valor)
        self.efeito = efeito
        self.duracao = duracao
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert consumable to dictionary
        
        Returns:
            Dictionary representation of the consumable
        """
        data = super().to_dict()
        data.update({
            "efeito": self.efeito,
            "duracao": self.duracao
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Consumivel':
        """
        Create consumable from dictionary
        
        Args:
            data: Dictionary with consumable data
            
        Returns:
            New consumable instance
        """
        consumivel = cls(
            data["nome"],
            data["descricao"],
            data["efeito"],
            data.get("duracao", 0),
            data.get("valor", 0)
        )
        
        if "id" in data:
            consumivel.id = data["id"]
        
        return consumivel


class Inventario:
    """
    Inventory manager for handling items.
    """
    
    def __init__(self, capacidade_maxima: int = 20):
        """
        Initialize a new inventory
        
        Args:
            capacidade_maxima: Maximum number of items
        """
        self.itens = []
        self.capacidade_maxima = capacidade_maxima
        self.equipados = {
            "arma": None,
            "armadura": None,
            "acessorio": None
        }
    
    def adicionar_item(self, item: Item) -> bool:
        """
        Add an item to the inventory
        
        Args:
            item: The item to add
            
        Returns:
            True if successful, False if inventory is full
        """
        if len(self.itens) >= self.capacidade_maxima:
            return False
        
        self.itens.append(item)
        return True
    
    def remover_item(self, item_id: str) -> Optional[Item]:
        """
        Remove an item from inventory
        
        Args:
            item_id: ID of the item to remove
            
        Returns:
            The removed item if found, None otherwise
        """
        for i, item in enumerate(self.itens):
            if item.id == item_id:
                return self.itens.pop(i)
        return None
    
    def obter_item(self, item_id: str) -> Optional[Item]:
        """
        Get an item from inventory
        
        Args:
            item_id: ID of the item
            
        Returns:
            The item if found, None otherwise
        """
        for item in self.itens:
            if item.id == item_id:
                return item
        return None
    
    def equipar_item(self, item_id: str) -> bool:
        """
        Equip an item
        
        Args:
            item_id: ID of the item to equip
            
        Returns:
            True if successful, False otherwise
        """
        item = self.obter_item(item_id)
        if not item:
            return False
        
        if item.tipo not in self.equipados:
            return False
        
        # Unequip current item in that slot if any
        if self.equipados[item.tipo]:
            self.desequipar_item(self.equipados[item.tipo].id)
        
        # Equip new item
        self.equipados[item.tipo] = item
        return True
    
    def desequipar_item(self, item_id: str) -> bool:
        """
        Unequip an item
        
        Args:
            item_id: ID of the item to unequip
            
        Returns:
            True if successful, False otherwise
        """
        for slot, item in self.equipados.items():
            if item and item.id == item_id:
                self.equipados[slot] = None
                return True
        return False
    
    def listar_itens_por_tipo(self, tipo: str) -> List[Item]:
        """
        List items of a specific type
        
        Args:
            tipo: Item type to filter by
            
        Returns:
            List of matching items
        """
        return [item for item in self.itens if item.tipo == tipo]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert inventory to dictionary
        
        Returns:
            Dictionary representation of the inventory
        """
        return {
            "capacidade_maxima": self.capacidade_maxima,
            "itens": [item.to_dict() for item in self.itens],
            "equipados": {
                slot: (item.to_dict() if item else None) 
                for slot, item in self.equipados.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Inventario':
        """
        Create inventory from dictionary
        
        Args:
            data: Dictionary with inventory data
            
        Returns:
            New inventory instance
        """
        inventario = cls(data.get("capacidade_maxima", 20))
        
        # Load items
        if "itens" in data:
            for item_data in data["itens"]:
                if item_data["tipo"] == "arma":
                    item = Arma.from_dict(item_data)
                elif item_data["tipo"] == "armadura":
                    item = Armadura.from_dict(item_data)
                elif item_data["tipo"] == "consumivel":
                    item = Consumivel.from_dict(item_data)
                else:
                    item = Item.from_dict(item_data)
                
                inventario.adicionar_item(item)
        
        # Load equipped items
        if "equipados" in data:
            for slot, item_data in data["equipados"].items():
                if item_data:
                    item = inventario.obter_item(item_data["id"])
                    if item:
                        inventario.equipados[slot] = item
        
        return inventario


# Factory for creating common items
class FabricaItens:
    """
    Factory for creating common game items.
    """
    
    @staticmethod
    def criar_espada_basica() -> Arma:
        """
        Create a basic sword
        
        Returns:
            New sword instance
        """
        espada = Arma(
            "Espada Básica",
            "Uma espada simples de aço.",
            5,  # dano
            "forca",
            False,  # uma mão
            10  # valor
        )
        return espada
    
    @staticmethod
    def criar_arco_basico() -> Arma:
        """
        Create a basic bow
        
        Returns:
            New bow instance
        """
        arco = Arma(
            "Arco Básico",
            "Um arco simples de madeira.",
            4,  # dano
            "destreza",
            True,  # duas mãos
            12  # valor
        )
        return arco
    
    @staticmethod
    def criar_cajado_basico() -> Arma:
        """
        Create a basic staff
        
        Returns:
            New staff instance
        """
        cajado = Arma(
            "Cajado Básico",
            "Um cajado simples de madeira com foco mágico.",
            3,  # dano
            "inteligencia",
            True,  # duas mãos
            15  # valor
        )
        
        # Add intelligence bonus
        cajado.adicionar_bonus("inteligencia", 2)
        
        return cajado
    
    @staticmethod
    def criar_armadura_leve() -> Armadura:
        """
        Create light armor
        
        Returns:
            New light armor instance
        """
        armadura = Armadura(
            "Armadura de Couro",
            "Uma armadura leve feita de couro tratado.",
            3,  # defesa
            "leve",
            0,  # sem requisito de força
            20  # valor
        )
        
        # Add dexterity bonus
        armadura.adicionar_bonus("destreza", 1)
        
        return armadura
    
    @staticmethod
    def criar_armadura_media() -> Armadura:
        """
        Create medium armor
        
        Returns:
            New medium armor instance
        """
        armadura = Armadura(
            "Cota de Malha",
            "Uma armadura média feita de anéis metálicos entrelaçados.",
            5,  # defesa
            "média",
            3,  # requisito de força
            35  # valor
        )
        
        # Add constitution bonus, but small dexterity penalty
        armadura.adicionar_bonus("constituicao", 1)
        armadura.adicionar_penalidade("destreza", -1)
        
        return armadura
    
    @staticmethod
    def criar_armadura_pesada() -> Armadura:
        """
        Create heavy armor
        
        Returns:
            New heavy armor instance
        """
        armadura = Armadura(
            "Armadura de Placas",
            "Uma armadura pesada feita de placas metálicas.",
            8,  # defesa
            "pesada",
            6,  # requisito de força
            50  # valor
        )
        
        # Add constitution bonus, but significant dexterity penalty
        armadura.adicionar_bonus("constituicao", 2)
        armadura.adicionar_penalidade("destreza", -2)
        
        return armadura
    
    @staticmethod
    def criar_pocao_cura() -> Consumivel:
        """
        Create healing potion
        
        Returns:
            New healing potion instance
        """
        pocao = Consumivel(
            "Poção de Cura",
            "Restaura pontos de vida quando consumida.",
            {"tipo": "cura", "valor": 30},
            0,  # efeito instantâneo
            15  # valor
        )
        return pocao
    
    @staticmethod
    def criar_pocao_forca() -> Consumivel:
        """
        Create strength potion
        
        Returns:
            New strength potion instance
        """
        pocao = Consumivel(
            "Poção de Força",
            "Aumenta temporariamente a força do personagem.",
            {"tipo": "bonus", "atributo": "forca", "valor": 3},
            3,  # duração (turnos)
            20  # valor
        )
        return pocao