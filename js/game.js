/**
 * Simulador de Batalha - Lógica do Jogo
 */

class Character {
    constructor(name, health, strength, defense) {
        this.name = name;
        this.maxHealth = health;
        this.health = health;
        this.strength = strength;
        this.defense = defense;
        this.isDefending = false;
        this.specialAttackCooldown = 0;
    }

    attack(target) {
        // Calculate base damage
        let damage = Math.floor(Math.random() * this.strength) + Math.floor(this.strength / 2);
        
        // Apply defense reduction
        if (target.isDefending) {
            // Defense reduces damage by 60% when defending
            damage = Math.max(1, Math.floor(damage * 0.4));
        } else {
            // Normal defense reduces damage by its value
            damage = Math.max(1, damage - Math.floor(Math.random() * target.defense));
        }
        
        // Apply damage
        target.health = Math.max(0, target.health - damage);
        
        // Reset defending status of target
        target.isDefending = false;
        
        return damage;
    }
    
    specialAttack(target) {
        // Special attack does more damage but has a cooldown
        const multiplier = 1.8;
        let damage = Math.floor((Math.random() * this.strength + this.strength) * multiplier);
        
        // Apply reduced defense effect
        damage = Math.max(1, damage - Math.floor(target.defense / 2));
        
        // Apply damage
        target.health = Math.max(0, target.health - damage);
        
        // Reset defending status of target
        target.isDefending = false;
        
        // Set cooldown
        this.specialAttackCooldown = 3;
        
        return damage;
    }

    heal() {
        // Heal 15-25% of max health
        const minHeal = Math.floor(this.maxHealth * 0.15);
        const maxHeal = Math.floor(this.maxHealth * 0.25);
        const healAmount = Math.floor(Math.random() * (maxHeal - minHeal + 1)) + minHeal;
        
        this.health = Math.min(this.maxHealth, this.health + healAmount);
        return healAmount;
    }
    
    defend() {
        this.isDefending = true;
        return true;
    }
    
    updateCooldowns() {
        if (this.specialAttackCooldown > 0) {
            this.specialAttackCooldown--;
        }
    }
}

class Game {
    constructor() {
        this.player = new Character('Jogador', 100, 10, 5);
        this.enemy = new Character('Inimigo', 100, 8, 3);
        this.round = 1;
        this.gameOver = false;
        this.winner = null;
        
        this.setupEventListeners();
        this.updateUI();
        this.addLogMessage('Batalha iniciada! Escolha sua ação.', 'system');
    }

    setupEventListeners() {
        document.getElementById('attack-btn').addEventListener('click', () => this.playerAction('attack'));
        document.getElementById('special-btn').addEventListener('click', () => this.playerAction('special'));
        document.getElementById('heal-btn').addEventListener('click', () => this.playerAction('heal'));
        document.getElementById('defend-btn').addEventListener('click', () => this.playerAction('defend'));
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
    }

    updateUI() {
        // Update health displays
        document.getElementById('player-health').textContent = this.player.health;
        document.getElementById('player-health-bar').style.width = `${(this.player.health / this.player.maxHealth) * 100}%`;
        
        document.getElementById('enemy-health').textContent = this.enemy.health;
        document.getElementById('enemy-health-bar').style.width = `${(this.enemy.health / this.enemy.maxHealth) * 100}%`;
        
        // Update stats
        document.getElementById('player-strength').textContent = this.player.strength;
        document.getElementById('player-defense').textContent = this.player.defense;
        
        document.getElementById('enemy-strength').textContent = this.enemy.strength;
        document.getElementById('enemy-defense').textContent = this.enemy.defense;
        
        // Update battle message
        if (this.gameOver) {
            document.getElementById('battle-message').textContent = this.winner === this.player ? 
                'Você venceu a batalha!' : 'Você foi derrotado!';
        } else {
            document.getElementById('battle-message').textContent = `Rodada ${this.round}`;
        }
        
        // Handle special attack button
        const specialBtn = document.getElementById('special-btn');
        if (this.player.specialAttackCooldown > 0) {
            specialBtn.textContent = `Ataque Especial (${this.player.specialAttackCooldown})`;
            specialBtn.classList.add('disabled');
        } else {
            specialBtn.textContent = 'Ataque Especial';
            specialBtn.classList.remove('disabled');
        }
        
        // Disable buttons if game is over
        const buttons = document.querySelectorAll('.controls .btn');
        if (this.gameOver) {
            buttons.forEach(btn => {
                if (btn.id !== 'reset-btn') {
                    btn.classList.add('disabled');
                }
            });
        } else {
            buttons.forEach(btn => {
                if (!(btn.id === 'special-btn' && this.player.specialAttackCooldown > 0)) {
                    btn.classList.remove('disabled');
                }
            });
        }
        
        // Add victory/defeat styling
        const playerEl = document.querySelector('.character.player');
        const enemyEl = document.querySelector('.character.enemy');
        
        if (this.gameOver) {
            if (this.winner === this.player) {
                playerEl.classList.add('victory');
                enemyEl.classList.add('defeat');
            } else {
                playerEl.classList.add('defeat');
                enemyEl.classList.add('victory');
            }
        } else {
            playerEl.classList.remove('victory', 'defeat');
            enemyEl.classList.remove('victory', 'defeat');
        }
    }

    addLogMessage(message, type = 'normal') {
        const logDiv = document.getElementById('log-messages');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        // Add class based on message type
        if (type === 'player') {
            logEntry.innerHTML = `<span class="player-action">${message}</span>`;
        } else if (type === 'enemy') {
            logEntry.innerHTML = `<span class="enemy-action">${message}</span>`;
        } else if (type === 'heal') {
            logEntry.innerHTML = `<span class="heal-action">${message}</span>`;
        } else if (type === 'special') {
            logEntry.innerHTML = `<span class="special-action">${message}</span>`;
        } else if (type === 'system') {
            logEntry.innerHTML = `<em>${message}</em>`;
        } else {
            logEntry.textContent = message;
        }
        
        logDiv.insertBefore(logEntry, logDiv.firstChild);
        
        // Auto-scroll to latest message
        logDiv.scrollTop = 0;
    }

    playerAction(action) {
        if (this.gameOver) return;
        
        // Prevent special attack if on cooldown
        if (action === 'special' && this.player.specialAttackCooldown > 0) {
            return;
        }
        
        // Handle player action
        switch (action) {
            case 'attack':
                const damage = this.player.attack(this.enemy);
                this.addLogMessage(`${this.player.name} atacou e causou ${damage} de dano ao ${this.enemy.name}!`, 'player');
                
                // Add visual effect
                document.querySelector('.character.enemy').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.character.enemy').classList.remove('shake');
                }, 500);
                break;
                
            case 'special':
                const specialDamage = this.player.specialAttack(this.enemy);
                this.addLogMessage(`${this.player.name} usou ataque especial e causou ${specialDamage} de dano ao ${this.enemy.name}!`, 'special');
                
                // Add visual effect
                document.querySelector('.character.enemy').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.character.enemy').classList.remove('shake');
                }, 500);
                break;
                
            case 'heal':
                const healAmount = this.player.heal();
                this.addLogMessage(`${this.player.name} se curou em ${healAmount} pontos de vida!`, 'heal');
                
                // Add visual effect
                document.querySelector('.character.player').classList.add('pulse');
                setTimeout(() => {
                    document.querySelector('.character.player').classList.remove('pulse');
                }, 500);
                break;
                
            case 'defend':
                this.player.defend();
                this.addLogMessage(`${this.player.name} está se defendendo para o próximo ataque!`, 'player');
                break;
        }
        
        this.updateUI();
        
        // Check if enemy is defeated
        if (this.enemy.health <= 0) {
            this.gameOver = true;
            this.winner = this.player;
            this.addLogMessage(`${this.enemy.name} foi derrotado! Você venceu!`, 'system');
            this.updateUI();
            return;
        }
        
        // Enemy's turn (after a short delay)
        setTimeout(() => {
            this.enemyTurn();
            
            // Start new round
            this.round++;
            
            // Update cooldowns
            this.player.updateCooldowns();
            this.enemy.updateCooldowns();
            
            this.updateUI();
        }, 1000);
    }
    
    enemyTurn() {
        if (this.gameOver) return;
        
        // Simple AI for enemy
        let action;
        
        if (this.enemy.health < this.enemy.maxHealth * 0.3 && Math.random() < 0.7) {
            // Heal if low on health (70% chance)
            action = 'heal';
        } else if (this.enemy.specialAttackCooldown <= 0 && Math.random() < 0.4) {
            // Use special attack if available (40% chance)
            action = 'special';
        } else if (this.player.isDefending === false && Math.random() < 0.2) {
            // Defend sometimes (20% chance)
            action = 'defend';
        } else {
            // Regular attack
            action = 'attack';
        }
        
        // Execute the chosen action
        switch (action) {
            case 'attack':
                const damage = this.enemy.attack(this.player);
                this.addLogMessage(`${this.enemy.name} atacou e causou ${damage} de dano ao ${this.player.name}!`, 'enemy');
                
                // Add visual effect
                document.querySelector('.character.player').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.character.player').classList.remove('shake');
                }, 500);
                break;
                
            case 'special':
                const specialDamage = this.enemy.specialAttack(this.player);
                this.addLogMessage(`${this.enemy.name} usou ataque especial e causou ${specialDamage} de dano ao ${this.player.name}!`, 'special');
                
                // Add visual effect
                document.querySelector('.character.player').classList.add('shake');
                setTimeout(() => {
                    document.querySelector('.character.player').classList.remove('shake');
                }, 500);
                break;
                
            case 'heal':
                const healAmount = this.enemy.heal();
                this.addLogMessage(`${this.enemy.name} se curou em ${healAmount} pontos de vida!`, 'heal');
                
                // Add visual effect
                document.querySelector('.character.enemy').classList.add('pulse');
                setTimeout(() => {
                    document.querySelector('.character.enemy').classList.remove('pulse');
                }, 500);
                break;
                
            case 'defend':
                this.enemy.defend();
                this.addLogMessage(`${this.enemy.name} está se defendendo para o próximo ataque!`, 'enemy');
                break;
        }
        
        // Check if player is defeated
        if (this.player.health <= 0) {
            this.gameOver = true;
            this.winner = this.enemy;
            this.addLogMessage(`${this.player.name} foi derrotado! Game Over!`, 'system');
        }
    }
    
    resetGame() {
        // Reset game state
        this.player = new Character('Jogador', 100, 10, 5);
        this.enemy = new Character('Inimigo', 100, 8, 3);
        this.round = 1;
        this.gameOver = false;
        this.winner = null;
        
        // Reset UI
        this.updateUI();
        
        // Clear log
        document.getElementById('log-messages').innerHTML = '';
        
        // Add starting message
        this.addLogMessage('Batalha reiniciada! Escolha sua ação.', 'system');
    }
}

// Start the game when the page loads
window.addEventListener('DOMContentLoaded', () => {
    new Game();
}); 