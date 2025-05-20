/**
 * Simulador de Batalha - Histórico de Batalhas
 */

// Elementos DOM
const noHistoryMsg = document.getElementById('no-history');
const historyList = document.getElementById('history-list');
const detailsModal = document.getElementById('battle-details-modal');
const modalTitle = document.getElementById('modal-title');
const modalCombatants = document.getElementById('modal-combatants');
const modalBattleInfo = document.getElementById('modal-battle-info');
const modalBattleLog = document.getElementById('modal-battle-log');
const closeModalBtn = document.getElementById('close-modal');

// Estado
let currentBattleId = null;

// Funções
function loadBattleHistory() {
    const battleHistory = DataManager.getBattleHistory();
    
    // Verificar se o histórico está vazio
    if (battleHistory.length === 0) {
        noHistoryMsg.style.display = 'block';
        historyList.innerHTML = '';
        return;
    }
    
    // Esconder mensagem de vazio
    noHistoryMsg.style.display = 'none';
    
    // Limpar lista
    historyList.innerHTML = '';
    
    // Renderizar cada batalha
    battleHistory.forEach(battle => {
        const winner = battle.winner === 'player1' ? battle.player1 : battle.player2;
        const loser = battle.winner === 'player1' ? battle.player2 : battle.player1;
        
        const battleCard = document.createElement('div');
        battleCard.className = 'battle-record';
        battleCard.dataset.battleId = battle.id;
        
        battleCard.innerHTML = `
            <div class="battle-record-header">
                <div class="battle-date">${formatDate(battle.date)}</div>
                <div class="battle-turn-count">Turnos: ${battle.turns}</div>
            </div>
            <div class="battle-record-content">
                <div class="battle-participants">
                    <div class="participant winner">
                        <div class="participant-avatar ${winner.class}-icon"></div>
                        <div class="participant-info">
                            <h4>${winner.name}</h4>
                            <div class="participant-class ${winner.class}">${CHARACTER_CLASSES[winner.class].name}</div>
                            <div class="winner-badge">Vencedor</div>
                        </div>
                    </div>
                    
                    <div class="versus-sign">VS</div>
                    
                    <div class="participant">
                        <div class="participant-avatar ${loser.class}-icon"></div>
                        <div class="participant-info">
                            <h4>${loser.name}</h4>
                            <div class="participant-class ${loser.class}">${CHARACTER_CLASSES[loser.class].name}</div>
                        </div>
                    </div>
                </div>
                <button class="btn details-btn" data-battle-id="${battle.id}">Ver Detalhes</button>
            </div>
        `;
        
        historyList.appendChild(battleCard);
    });
    
    // Adicionar listeners para botões de detalhes
    document.querySelectorAll('.details-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const battleId = this.getAttribute('data-battle-id');
            openBattleDetails(battleId);
        });
    });
}

function openBattleDetails(battleId) {
    const battleHistory = DataManager.getBattleHistory();
    const battle = battleHistory.find(b => b.id === battleId);
    
    if (!battle) return;
    
    currentBattleId = battleId;
    
    // Preencher título
    modalTitle.textContent = `Batalha - ${formatDate(battle.date)}`;
    
    // Preencher combatentes
    const winner = battle.winner === 'player1' ? battle.player1 : battle.player2;
    const loser = battle.winner === 'player1' ? battle.player2 : battle.player1;
    
    modalCombatants.innerHTML = `
        <div class="modal-participants">
            <div class="modal-participant winner">
                <div class="participant-avatar ${winner.class}-icon"></div>
                <div class="participant-info">
                    <h4>${winner.name}</h4>
                    <div class="participant-class">${CHARACTER_CLASSES[winner.class].name}</div>
                    <div class="winner-badge">Vencedor</div>
                    <div class="final-health">Vida final: ${winner.finalHealth}</div>
                </div>
            </div>
            
            <div class="versus-sign">VS</div>
            
            <div class="modal-participant">
                <div class="participant-avatar ${loser.class}-icon"></div>
                <div class="participant-info">
                    <h4>${loser.name}</h4>
                    <div class="participant-class">${CHARACTER_CLASSES[loser.class].name}</div>
                    <div class="final-health">Vida final: ${loser.finalHealth}</div>
                </div>
            </div>
        </div>
    `;
    
    // Preencher informações da batalha
    modalBattleInfo.innerHTML = `
        <div class="battle-stats">
            <div class="battle-stat">
                <div class="stat-label">Data</div>
                <div class="stat-value">${formatDate(battle.date)}</div>
            </div>
            <div class="battle-stat">
                <div class="stat-label">Turnos</div>
                <div class="stat-value">${battle.turns}</div>
            </div>
            <div class="battle-stat">
                <div class="stat-label">Total de Ações</div>
                <div class="stat-value">${battle.log.length}</div>
            </div>
        </div>
    `;
    
    // Preencher log da batalha
    modalBattleLog.innerHTML = '';
    if (battle.log && battle.log.length > 0) {
        const logEntries = document.createElement('div');
        logEntries.className = 'log-entries';
        
        battle.log.forEach(entry => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            
            // Adicionar classe baseada no tipo de mensagem
            switch (entry.type) {
                case 'attack':
                    logEntry.innerHTML = `<span class="log-attack">${entry.message}</span>`;
                    break;
                case 'special':
                    logEntry.innerHTML = `<span class="log-special">${entry.message}</span>`;
                    break;
                case 'heal':
                    logEntry.innerHTML = `<span class="log-heal">${entry.message}</span>`;
                    break;
                case 'defend':
                    logEntry.innerHTML = `<span class="log-defend">${entry.message}</span>`;
                    break;
                case 'turn':
                    logEntry.innerHTML = `<span class="log-turn">${entry.message}</span>`;
                    break;
                case 'system':
                    logEntry.innerHTML = `<span class="log-system">${entry.message}</span>`;
                    break;
                default:
                    logEntry.textContent = entry.message;
            }
            
            logEntries.appendChild(logEntry);
        });
        
        modalBattleLog.appendChild(logEntries);
    } else {
        modalBattleLog.innerHTML = '<div class="empty-log">Não há registros de ações para esta batalha.</div>';
    }
    
    // Exibir modal
    detailsModal.classList.add('open');
}

function closeModal() {
    detailsModal.classList.remove('open');
    currentBattleId = null;
}

// Event Listeners
closeModalBtn.addEventListener('click', closeModal);

// Fechar modal ao clicar fora dele
window.addEventListener('click', function(event) {
    if (event.target === detailsModal) {
        closeModal();
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadBattleHistory();
}); 