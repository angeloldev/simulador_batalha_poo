# 🧙‍♂️ Medieval Fantasy Battle Simulator

A turn-based character battle simulator set in a rich medieval fantasy world. This project demonstrates comprehensive object-oriented programming principles while providing an engaging battle simulation experience.

## 📌 Project Overview

This battle simulator allows players to create and customize characters from different classes (Warrior, Mage, Archer), equip them with various items, and engage in turn-based battles. The project showcases object-oriented programming concepts including inheritance, polymorphism, mixins, composition, and association.

## 🌍 Universe & Context

The simulator is set in the realm of Eldoria, a medieval fantasy world where magic and martial prowess coexist. Various character classes harness different powers:

- **Warriors**: Masters of physical combat with superior strength and defensive capabilities
- **Mages**: Wielders of arcane magic with powerful spells but limited physical defense
- **Archers**: Ranged specialists with high accuracy and critical strike potential

## 📝 Use Cases

### Creating a Character
1. User selects a character class (Warrior, Mage, Archer)
2. User customizes character attributes (name, appearance, stats)
3. User assigns initial equipment
4. System saves the character

### Initiating a Battle
1. User selects two characters for battle
2. System initializes the battle arena
3. Battle proceeds with turn-based actions
4. System records and displays battle actions
5. Winner is determined when one character's health reaches zero

### Managing Character Inventory
1. User selects a character
2. User adds, removes, or equips items
3. System updates character stats based on equipment
4. Changes are saved

### Saving/Loading Progress
1. User selects save option
2. System serializes character data
3. System stores data in persistent storage
4. User can load saved characters later

## 📊 Class Diagram

```
+-------------------+       +-------------------+       +-------------------+
|    Personagem     |<------|     Combate       |       |   Habilidade      |
+-------------------+       +-------------------+       +-------------------+
| - nome            |       | - personagem1     |       | - nome            |
| - nivel           |       | - personagem2     |       | - descricao       |
| - vida            |       | - turno_atual     |       | - custo           |
| - forca           |       | - log_combate     |       | - efeito          |
| # habilidades     |       +-------------------+       +-------------------+
| # inventario      |       | + iniciar()       |               ▲
+-------------------+       | + proximo_turno() |               |
| + atacar()        |       | + finalizar()     |    +---------+---------+
| + defender()      |       +-------------------+    |                   |
| + usar_habilidade()|                               |                   |
+-------------------+                          +-------------+   +-------------+
         ▲                                     | Magica      |   | Fisica      |
         |                                     +-------------+   +-------------+
+--------+--------+                            | - mana      |   | - stamina   |
|                 |                            +-------------+   +-------------+
|                 |
+--------+--------+--------+
|        |        |        |
+--------+  +-----+  +-----+
| Guerreiro | Mago  | Arqueiro |
+--------+  +-----+  +-----+
| + furia   | + mana | + precisao|
+---------+ +------+ +-------+
```

## 🛠️ Technologies Used

- **Python 3.10+**: Core logic and OOP implementation
- **Flask**: Web server for the frontend
- **HTML/CSS**: User interface design
- **Pickle/JSON**: Data serialization for saving/loading state

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Open the web interface at `http://localhost:5000`

## 🔄 Project Structure

```
simulador_batalha/
├── README.md
├── main.py
├── requirements.txt
├── package/
│   ├── personagens/
│   │   ├── base.py
│   │   ├── guerreiro.py
│   │   ├── mago.py
│   │   ├── arqueiro.py
│   │   ├── mixins.py
│   ├── combate.py
│   ├── habilidades.py
│   ├── inventario.py
│   ├── banco.py
├── templates/
│   ├── index.html
│   ├── create.html
│   ├── battle.html
│   ├── inventory.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   ├── images/
```

## 📈 Evaluation Criteria

- Program functionality with all required features (6 pts)
- OOP modeling with inheritance, polymorphism, mixins, composition, association (6 pts)
- Object serialization for saving character state (6 pts)
- Functional and clear graphical interface (2 pts)