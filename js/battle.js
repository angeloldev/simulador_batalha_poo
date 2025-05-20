/**
 * Simulador de Batalha - Sistema de Batalha
 */

// Estado da batalha
let battleState = {
    turn: 1,
    player1: null,
    player2: null,
    activePlayer: null,
    inactivePlayer: null,
    isGameOver: false,
    winner: null,
    battleLog: []
};

// Elementos DOM
const player1Container = document.getElementById('player1-container');
const player2Container = document.getElementById('player2-container');
const player1Name = document.getElementById('player1-name');
const player2Name = document.getElementById('player2-name');
const player1Avatar = document.getElementById('player1-avatar');
const player2Avatar = document.getElementById('player2-avatar');
const player1Health = document.getElementById('player1-health');
const player2Health = document.getElementById('player2-health');
const player1MaxHealth = document.getElementById('player1-max-health');
const player2MaxHealth = document.getElementById('player2-max-health');
const player1HealthBar = document.getElementById('player1-health-bar');
const player2HealthBar = document.getElementById('player2-health-bar');
const player1Strength = document.getElementById('player1-strength');
const player2Strength = document.getElementById('player2-strength');
const player1Defense = document.getElementById('player1-defense');
const player2Defense = document.getElementById('player2-defense');
const player1Status = document.getElementById('player1-status');
const player2Status = document.getElementById('player2-status');
const activePlayerInfo = document.getElementById('active-player-info');
const activePlayerName = document.getElementById('active-player-name');
const battleMessage = document.getElementById('battle-message');
const turnCounter = document.getElementById('turn-counter');
const logMessages = document.getElementById('log-messages');
const attackBtn = document.getElementById('attack-btn');
const specialBtn = document.getElementById('special-btn');
const healBtn = document.getElementById('heal-btn');
const defendBtn = document.getElementById('defend-btn');
const battleResult = document.getElementById('battle-result');
const winnerMessage = document.getElementById('winner-message');
const returnBtn = document.getElementById('return-btn');
const saveBattleBtn = document.getElementById('save-battle-btn');

// Classe para personagem de batalha
class BattleCharacter {
    constructor(character) {
        this.id = character.id;
        this.name = character.name;
        this.class = character.class;
        this.maxHealth = character.health;
        this.health = character.health;
        this.strength = character.strength;
        this.defense = character.defense;
        this.abilities = character.abilities || [];
        this.isDefending = false;
        this.specialCooldown = 0;
    }
    
    attack(target) {
        // Cálculo de dano básico
        let damage = Math.floor(Math.random() * this.strength) + Math.floor(this.strength / 2);
        
        // Aplicar redução de defesa
        if (target.isDefending) {
            // Defesa reduz o dano em 60% quando defendendo
            damage = Math.max(1, Math.floor(damage * 0.4));
        } else {
            // Defesa normal reduz o dano pelo seu valor
            damage = Math.max(1, damage - Math.floor(Math.random() * target.defense));
        }
        
        // Aplicar dano
        target.health = Math.max(0, target.health - damage);
        
        // Resetar status de defesa do alvo
        target.isDefending = false;
        
        return damage;
    }
    
    specialAttack(target) {
        // Ataque especial causa mais dano mas tem cooldown
        const multiplier = 1.8;
        let damage = Math.floor((Math.random() * this.strength + this.strength) * multiplier);
        
        // Aplicar redução de defesa reduzida
        damage = Math.max(1, damage - Math.floor(target.defense / 2));
        
        // Aplicar dano
        target.health = Math.max(0, target.health - damage);
        
        // Resetar status de defesa do alvo
        target.isDefending = false;
        
        // Definir cooldown
        this.specialCooldown = 3;
        
        return damage;
    }
    
    heal() {
        // Curar 15-25% da vida máxima
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
        if (this.specialCooldown > 0) {
            this.specialCooldown--;
        }
    }
}

// Funções
function initBattle() {
    // Recuperar os IDs dos personagens selecionados
    const player1Id = sessionStorage.getItem('player1');
    const player2Id = sessionStorage.getItem('player2');
    
    if (!player1Id || !player2Id) {
        // Redirecionar de volta para a seleção se não houver personagens
        window.location.href = 'battle-select.html';
        return;
    }
    
    // Carregar os personagens
    const player1Data = DataManager.getCharacter(player1Id);
    const player2Data = DataManager.getCharacter(player2Id);
    
    if (!player1Data || !player2Data) {
        window.location.href = 'battle-select.html';
        return;
    }
    
    // Inicializar personagens de batalha
    battleState.player1 = new BattleCharacter(player1Data);
    battleState.player2 = new BattleCharacter(player2Data);
    
    // Definir jogador ativo (player1 começa)
    battleState.activePlayer = battleState.player1;
    battleState.inactivePlayer = battleState.player2;
    
    // Atualizar a interface
    updateBattleUI();
    
    // Adicionar log inicial
    addLogMessage('Batalha iniciada entre ' + battleState.player1.name + ' e ' + battleState.player2.name + '!', 'system');
    addLogMessage('Turno 1: ' + battleState.player1.name + ' começa!', 'turn');
}

function updateBattleUI() {
    // Atualizar informações do player1
    player1Name.textContent = battleState.player1.name;
    player1Avatar.className = `character-avatar ${battleState.player1.class}-icon`;
    player1Health.textContent = battleState.player1.health;
    player1MaxHealth.textContent = battleState.player1.maxHealth;
    player1HealthBar.style.width = `${(battleState.player1.health / battleState.player1.maxHealth) * 100}%`;
    player1Strength.textContent = battleState.player1.strength;
    player1Defense.textContent = battleState.player1.defense;
    
    // Atualizar informações do player2
    player2Name.textContent = battleState.player2.name;
    player2Avatar.className = `character-avatar ${battleState.player2.class}-icon`;
    player2Health.textContent = battleState.player2.health;
    player2MaxHealth.textContent = battleState.player2.maxHealth;
    player2HealthBar.style.width = `${(battleState.player2.health / battleState.player2.maxHealth) * 100}%`;
    player2Strength.textContent = battleState.player2.strength;
    player2Defense.textContent = battleState.player2.defense;
    
    // Atualizar turno e mensagem
    turnCounter.textContent = `Turno ${battleState.turn}`;
    
    // Destacar jogador ativo
    if (battleState.activePlayer === battleState.player1) {
        player1Container.classList.add('active');
        player2Container.classList.remove('active');
        activePlayerName.textContent = battleState.player1.name;
    } else {
        player1Container.classList.remove('active');
        player2Container.classList.add('active');
        activePlayerName.textContent = battleState.player2.name;
    }
    
    // Atualizar status de defesa
    player1Status.innerHTML = battleState.player1.isDefending ? '<span class="defending-status">Defendendo</span>' : '';
    player2Status.innerHTML = battleState.player2.isDefending ? '<span class="defending-status">Defendendo</span>' : '';
    
    // Atualizar botão de ataque especial
    if (battleState.activePlayer.specialCooldown > 0) {
        specialBtn.textContent = `Ataque Especial (${battleState.activePlayer.specialCooldown})`;
        specialBtn.disabled = true;
        specialBtn.classList.add('disabled');
    } else {
        specialBtn.textContent = 'Ataque Especial';
        specialBtn.disabled = false;
        specialBtn.classList.remove('disabled');
    }
    
    // Se o jogo acabou, mostrar o resultado
    if (battleState.isGameOver) {
        showBattleResult();
    }
}

function performAction(action) {
    if (battleState.isGameOver) return;
    
    let logMessage = '';
    const activePlayer = battleState.activePlayer;
    const inactivePlayer = battleState.inactivePlayer;
    
    // Executar ação selecionada
    switch (action) {
        case 'attack':
            const damage = activePlayer.attack(inactivePlayer);
            logMessage = `${activePlayer.name} atacou e causou ${damage} de dano a ${inactivePlayer.name}!`;
            addLogMessage(logMessage, 'attack');
            
            // Efeito visual
            if (inactivePlayer === battleState.player1) {
                player1Container.classList.add('shake');
                setTimeout(() => player1Container.classList.remove('shake'), 500);
            } else {
                player2Container.classList.add('shake');
                setTimeout(() => player2Container.classList.remove('shake'), 500);
            }
            break;
            
        case 'special':
            if (activePlayer.specialCooldown > 0) return; // Não deveria acontecer, mas por precaução
            
            const specialDamage = activePlayer.specialAttack(inactivePlayer);
            logMessage = `${activePlayer.name} usou ataque especial e causou ${specialDamage} de dano a ${inactivePlayer.name}!`;
            addLogMessage(logMessage, 'special');
            
            // Efeito visual
            if (inactivePlayer === battleState.player1) {
                player1Container.classList.add('shake');
                setTimeout(() => player1Container.classList.remove('shake'), 500);
            } else {
                player2Container.classList.add('shake');
                setTimeout(() => player2Container.classList.remove('shake'), 500);
            }
            break;
            
        case 'heal':
            const healAmount = activePlayer.heal();
            logMessage = `${activePlayer.name} se curou em ${healAmount} pontos de vida!`;
            addLogMessage(logMessage, 'heal');
            
            // Efeito visual
            if (activePlayer === battleState.player1) {
                player1Container.classList.add('pulse');
                setTimeout(() => player1Container.classList.remove('pulse'), 500);
            } else {
                player2Container.classList.add('pulse');
                setTimeout(() => player2Container.classList.remove('pulse'), 500);
            }
            break;
            
        case 'defend':
            activePlayer.defend();
            logMessage = `${activePlayer.name} está se defendendo para o próximo ataque!`;
            addLogMessage(logMessage, 'defend');
            break;
    }
    
    // Verificar se a batalha terminou
    if (inactivePlayer.health <= 0) {
        endBattle(activePlayer);
        return;
    }
    
    // Atualizar a interface
    updateBattleUI();
    
    // Alternar jogador ativo
    switchActivePlayer();
    
    // Atualizar cooldowns
    battleState.player1.updateCooldowns();
    battleState.player2.updateCooldowns();
    
    // Atualizar interface novamente para refletir o novo jogador ativo
    updateBattleUI();
}

function switchActivePlayer() {
    // Alternar jogador ativo
    if (battleState.activePlayer === battleState.player1) {
        battleState.activePlayer = battleState.player2;
        battleState.inactivePlayer = battleState.player1;
    } else {
        battleState.activePlayer = battleState.player1;
        battleState.inactivePlayer = battleState.player2;
        
        // Incrementar turno quando player1 fica ativo novamente
        battleState.turn++;
        addLogMessage(`Turno ${battleState.turn}`, 'turn');
    }
}

function endBattle(winner) {
    battleState.isGameOver = true;
    battleState.winner = winner;
    
    addLogMessage(`${winner.name} venceu a batalha!`, 'system');
    
    showBattleResult();
}

function showBattleResult() {
    // Desabilitar botões de ação
    attackBtn.disabled = true;
    specialBtn.disabled = true;
    healBtn.disabled = true;
    defendBtn.disabled = true;
    
    attackBtn.classList.add('disabled');
    specialBtn.classList.add('disabled');
    healBtn.classList.add('disabled');
    defendBtn.classList.add('disabled');
    
    // Exibir div de resultado
    battleResult.style.display = 'block';
    
    // Atualizar mensagem do vencedor
    winnerMessage.textContent = `${battleState.winner.name} venceu a batalha!`;
    
    // Adicionar classes de vitória/derrota aos personagens
    if (battleState.winner === battleState.player1) {
        player1Container.classList.add('victory');
        player2Container.classList.add('defeat');
    } else {
        player1Container.classList.add('defeat');
        player2Container.classList.add('victory');
    }
}

function addLogMessage(message, type = 'normal') {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    // Adicionar classe baseada no tipo de mensagem
    switch (type) {
        case 'attack':
            logEntry.innerHTML = `<span class="log-attack">${message}</span>`;
            break;
        case 'special':
            logEntry.innerHTML = `<span class="log-special">${message}</span>`;
            break;
        case 'heal':
            logEntry.innerHTML = `<span class="log-heal">${message}</span>`;
            break;
        case 'defend':
            logEntry.innerHTML = `<span class="log-defend">${message}</span>`;
            break;
        case 'turn':
            logEntry.innerHTML = `<span class="log-turn">${message}</span>`;
            break;
        case 'system':
            logEntry.innerHTML = `<span class="log-system">${message}</span>`;
            break;
        default:
            logEntry.textContent = message;
    }
    
    // Adicionar ao DOM
    logMessages.insertBefore(logEntry, logMessages.firstChild);
    
    // Salvar no histórico da batalha
    battleState.battleLog.push({
        message,
        type,
        turn: battleState.turn
    });
}

function saveBattleToHistory() {
    // Criar objeto de registro de batalha
    const battleRecord = {
        player1: {
            id: battleState.player1.id,
            name: battleState.player1.name,
            class: battleState.player1.class,
            finalHealth: battleState.player1.health
        },
        player2: {
            id: battleState.player2.id,
            name: battleState.player2.name,
            class: battleState.player2.class,
            finalHealth: battleState.player2.health
        },
        winner: battleState.winner === battleState.player1 ? 'player1' : 'player2',
        turns: battleState.turn,
        log: battleState.battleLog
    };
    
    // Salvar no histórico
    DataManager.saveBattleRecord(battleRecord);
    
    // Notificar usuário
    alert('Batalha salva no histórico!');
    
    // Redirecionar para histórico
    window.location.href = 'battle-history.html';
}

// Event Listeners
attackBtn.addEventListener('click', () => performAction('attack'));
specialBtn.addEventListener('click', () => performAction('special'));
healBtn.addEventListener('click', () => performAction('heal'));
defendBtn.addEventListener('click', () => performAction('defend'));

returnBtn.addEventListener('click', () => window.location.href = 'battle-select.html');
saveBattleBtn.addEventListener('click', saveBattleToHistory);

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initBattle();
}); 