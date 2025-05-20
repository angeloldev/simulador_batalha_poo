/**
 * Simulador de Batalha - Seleção de Personagens para Batalha
 */

// Elementos DOM
const notEnoughCharactersMsg = document.getElementById('not-enough-characters');
const selectionContent = document.getElementById('selection-content');
const player1Select = document.getElementById('player1-select');
const player2Select = document.getElementById('player2-select');
const player1Preview = document.getElementById('player1-preview');
const player2Preview = document.getElementById('player2-preview');
const startBattleBtn = document.getElementById('start-battle-btn');

// Funções
function initBattleSelection() {
    const characters = DataManager.getCharacters();
    
    // Verificar se tem pelo menos 2 personagens
    if (characters.length < 2) {
        notEnoughCharactersMsg.style.display = 'block';
        selectionContent.style.display = 'none';
        return;
    }
    
    // Mostrar conteúdo de seleção
    notEnoughCharactersMsg.style.display = 'none';
    selectionContent.style.display = 'block';
    
    // Preencher os selects
    populateCharacterSelects(characters);
}

function populateCharacterSelects(characters) {
    // Limpar opções existentes, exceto a primeira
    player1Select.innerHTML = '<option value="">Selecione um personagem...</option>';
    player2Select.innerHTML = '<option value="">Selecione um personagem...</option>';
    
    // Adicionar opções para cada personagem
    characters.forEach(character => {
        const option1 = document.createElement('option');
        option1.value = character.id;
        option1.textContent = `${character.name} (${CHARACTER_CLASSES[character.class].name})`;
        player1Select.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = character.id;
        option2.textContent = `${character.name} (${CHARACTER_CLASSES[character.class].name})`;
        player2Select.appendChild(option2);
    });
}

function updateCharacterPreview(selectElement, previewElement) {
    const characterId = selectElement.value;
    
    if (!characterId) {
        previewElement.innerHTML = '<div class="empty-preview">Selecione um personagem</div>';
        return;
    }
    
    const character = DataManager.getCharacter(characterId);
    if (!character) {
        previewElement.innerHTML = '<div class="empty-preview">Personagem não encontrado</div>';
        return;
    }
    
    const classData = CHARACTER_CLASSES[character.class];
    
    previewElement.innerHTML = `
        <div class="character-card-preview ${character.class}">
            <div class="character-avatar ${character.class}-icon"></div>
            <h3>${character.name}</h3>
            <div class="character-class-badge">${classData.name}</div>
            <div class="stats-preview">
                <div class="stat-item">
                    <div class="stat-label">Vida</div>
                    <div class="stat-value">${character.health}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Força</div>
                    <div class="stat-value">${character.strength}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Defesa</div>
                    <div class="stat-value">${character.defense}</div>
                </div>
            </div>
        </div>
    `;
}

function validateBattleSelection() {
    const player1Id = player1Select.value;
    const player2Id = player2Select.value;
    
    // Verificar se ambos os personagens foram selecionados
    if (!player1Id || !player2Id) {
        startBattleBtn.disabled = true;
        return;
    }
    
    // Verificar se não é o mesmo personagem
    if (player1Id === player2Id) {
        startBattleBtn.disabled = true;
        return;
    }
    
    // Tudo ok, habilitar botão
    startBattleBtn.disabled = false;
}

function startBattle() {
    const player1Id = player1Select.value;
    const player2Id = player2Select.value;
    
    if (!player1Id || !player2Id || player1Id === player2Id) {
        return; // Não deve acontecer, mas por precaução
    }
    
    // Salvar seleção no sessionStorage para usar na página da batalha
    sessionStorage.setItem('player1', player1Id);
    sessionStorage.setItem('player2', player2Id);
    
    // Redirecionar para a página da batalha
    window.location.href = 'battle.html';
}

// Event Listeners
player1Select.addEventListener('change', function() {
    updateCharacterPreview(player1Select, player1Preview);
    validateBattleSelection();
});

player2Select.addEventListener('change', function() {
    updateCharacterPreview(player2Select, player2Preview);
    validateBattleSelection();
});

startBattleBtn.addEventListener('click', startBattle);

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initBattleSelection();
}); 