class Character {
    constructor(name, health, strength) {
        this.name = name;
        this.health = health;
        this.strength = strength;
    }

    attack(target) {
        const damage = Math.floor(Math.random() * this.strength) + 1;
        target.health -= damage;
        return damage;
    }

    heal() {
        const healAmount = Math.floor(Math.random() * 10) + 5;
        this.health = Math.min(100, this.health + healAmount);
        return healAmount;
    }
}

class Game {
    constructor() {
        this.player = new Character('Jogador', 100, 10);
        this.enemy = new Character('Inimigo', 100, 10);
        this.setupEventListeners();
        this.updateUI();
    }

    setupEventListeners() {
        document.getElementById('attack-btn').addEventListener('click', () => this.playerTurn());
        document.getElementById('heal-btn').addEventListener('click', () => this.healPlayer());
    }

    updateUI() {
        document.getElementById('player-health').textContent = this.player.health;
        document.getElementById('player-strength').textContent = this.player.strength;
        document.getElementById('enemy-health').textContent = this.enemy.health;
        document.getElementById('enemy-strength').textContent = this.enemy.strength;
    }

    addLogMessage(message) {
        const logDiv = document.getElementById('log-messages');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = message;
        logDiv.insertBefore(logEntry, logDiv.firstChild);
    }

    playerTurn() {
        if (this.player.health <= 0 || this.enemy.health <= 0) return;

        // Player attacks
        const damage = this.player.attack(this.enemy);
        this.addLogMessage(`${this.player.name} causou ${damage} de dano ao ${this.enemy.name}!`);
        this.updateUI();

        if (this.enemy.health <= 0) {
            this.addLogMessage(`${this.enemy.name} foi derrotado! Você venceu!`);
            return;
        }

        // Enemy attacks
        setTimeout(() => {
            const enemyDamage = this.enemy.attack(this.player);
            this.addLogMessage(`${this.enemy.name} causou ${enemyDamage} de dano ao ${this.player.name}!`);
            this.updateUI();

            if (this.player.health <= 0) {
                this.addLogMessage(`${this.player.name} foi derrotado! Game Over!`);
            }
        }, 1000);
    }

    healPlayer() {
        if (this.player.health <= 0) return;

        const healAmount = this.player.heal();
        this.addLogMessage(`${this.player.name} se curou em ${healAmount} pontos de vida!`);
        this.updateUI();

        // Enemy attacks after healing
        setTimeout(() => {
            const enemyDamage = this.enemy.attack(this.player);
            this.addLogMessage(`${this.enemy.name} causou ${enemyDamage} de dano ao ${this.player.name}!`);
            this.updateUI();

            if (this.player.health <= 0) {
                this.addLogMessage(`${this.player.name} foi derrotado! Game Over!`);
            }
        }, 1000);
    }
}

// Start the game when the page loads
window.addEventListener('DOMContentLoaded', () => {
    new Game();
}); 