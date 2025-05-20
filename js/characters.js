/**
 * Simulador de Batalha - Gerenciamento de Personagens
 */

// Estado da aplicação
let currentCharacterId = null;

// Elementos DOM
const characterList = document.getElementById('character-list');
const emptyMessage = document.getElementById('empty-characters');
const characterModal = document.getElementById('character-modal');
const modalTitle = document.getElementById('modal-title');
const characterForm = document.getElementById('character-form');
const characterIdInput = document.getElementById('character-id');
const characterNameInput = document.getElementById('character-name');
const newCharacterBtn = document.getElementById('new-character-btn');
const closeModalBtn = document.getElementById('close-modal');
const cancelBtn = document.getElementById('cancel-btn');
const confirmDeleteModal = document.getElementById('confirm-delete-modal');
const confirmDeleteBtn = document.getElementById('confirm-delete');
const cancelDeleteBtn = document.getElementById('cancel-delete');
const closeConfirmBtn = document.getElementById('close-confirm');

// Funções
function renderCharacterList() {
    const characters = DataManager.getCharacters();
    
    // Mostrar mensagem de lista vazia se não houver personagens
    if (characters.length === 0) {
        emptyMessage.style.display = 'block';
        characterList.innerHTML = '';
        return;
    }
    
    // Esconder mensagem de lista vazia
    emptyMessage.style.display = 'none';
    
    // Renderizar cada personagem
    characterList.innerHTML = '';
    characters.forEach(character => {
        const classData = CHARACTER_CLASSES[character.class];
        
        const characterCard = document.createElement('div');
        characterCard.className = `character-card ${character.class}`;
        characterCard.innerHTML = `
            <div class="character-header">
                <div class="character-avatar ${character.class}-icon"></div>
                <div class="character-info">
                    <h3>${character.name}</h3>
                    <div class="character-class-badge">${classData.name}</div>
                </div>
            </div>
            <div class="character-stats">
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
            <div class="character-actions">
                <button class="btn edit-btn" data-id="${character.id}">Editar</button>
                <button class="btn delete-btn" data-id="${character.id}">Excluir</button>
            </div>
        `;
        
        characterList.appendChild(characterCard);
    });
    
    // Adicionar event listeners para os botões
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const characterId = this.getAttribute('data-id');
            openEditCharacterModal(characterId);
        });
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const characterId = this.getAttribute('data-id');
            openDeleteConfirmation(characterId);
        });
    });
}

function openNewCharacterModal() {
    // Limpar formulário
    characterForm.reset();
    characterIdInput.value = '';
    modalTitle.textContent = 'Novo Personagem';
    currentCharacterId = null;
    
    // Exibir modal
    characterModal.classList.add('open');
}

function openEditCharacterModal(characterId) {
    const character = DataManager.getCharacter(characterId);
    if (!character) return;
    
    // Preencher formulário
    characterIdInput.value = character.id;
    characterNameInput.value = character.name;
    document.querySelector(`#class-${character.class}`).checked = true;
    
    // Atualizar título e estado
    modalTitle.textContent = 'Editar Personagem';
    currentCharacterId = characterId;
    
    // Exibir modal
    characterModal.classList.add('open');
}

function closeCharacterModal() {
    characterModal.classList.remove('open');
}

function saveCharacter(event) {
    event.preventDefault();
    
    // Obter valores do formulário
    const characterId = characterIdInput.value;
    const name = characterNameInput.value.trim();
    const classValue = document.querySelector('input[name="character-class"]:checked').value;
    
    // Validar
    if (!name) {
        alert('Por favor, forneça um nome para o personagem.');
        return;
    }
    
    if (!classValue) {
        alert('Por favor, selecione uma classe para o personagem.');
        return;
    }
    
    // Obter estatísticas da classe
    const classData = CHARACTER_CLASSES[classValue];
    
    // Criar ou atualizar personagem
    const character = {
        id: characterId || null,
        name: name,
        class: classValue,
        health: classData.baseHealth,
        strength: classData.baseStrength,
        defense: classData.baseDefense,
        abilities: classData.abilities
    };
    
    // Salvar
    DataManager.saveCharacter(character);
    
    // Fechar modal e atualizar lista
    closeCharacterModal();
    renderCharacterList();
}

function openDeleteConfirmation(characterId) {
    currentCharacterId = characterId;
    confirmDeleteModal.classList.add('open');
}

function closeDeleteConfirmation() {
    confirmDeleteModal.classList.remove('open');
    currentCharacterId = null;
}

function deleteCharacter() {
    if (!currentCharacterId) return;
    
    DataManager.deleteCharacter(currentCharacterId);
    closeDeleteConfirmation();
    renderCharacterList();
}

// Event Listeners
newCharacterBtn.addEventListener('click', openNewCharacterModal);
closeModalBtn.addEventListener('click', closeCharacterModal);
cancelBtn.addEventListener('click', closeCharacterModal);
characterForm.addEventListener('submit', saveCharacter);

confirmDeleteBtn.addEventListener('click', deleteCharacter);
cancelDeleteBtn.addEventListener('click', closeDeleteConfirmation);
closeConfirmBtn.addEventListener('click', closeDeleteConfirmation);

// Seletor de classes
document.querySelectorAll('.class-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.class-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
    });
});

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    renderCharacterList();
}); 