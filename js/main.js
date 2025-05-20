/**
 * Simulador de Batalha - Script Principal
 * Gerencia funcionalidades compartilhadas entre páginas
 */

// Classes de personagens e suas características
const CHARACTER_CLASSES = {
    guerreiro: {
        name: 'Guerreiro',
        baseHealth: 120,
        baseStrength: 10,
        baseDefense: 8,
        icon: 'guerreiro-icon',
        description: 'Especialista em combate corpo a corpo com alta resistência e poder de ataque.',
        abilities: [
            { name: 'Golpe Poderoso', type: 'attack', multiplier: 1.5, cooldown: 2 },
            { name: 'Postura Defensiva', type: 'defense', multiplier: 2, cooldown: 3 }
        ]
    },
    mago: {
        name: 'Mago',
        baseHealth: 80,
        baseStrength: 14,
        baseDefense: 4,
        icon: 'mago-icon',
        description: 'Domina magias arcanas com alto poder de dano, mas baixa resistência.',
        abilities: [
            { name: 'Bola de Fogo', type: 'attack', multiplier: 1.8, cooldown: 2 },
            { name: 'Escudo Arcano', type: 'defense', multiplier: 1.5, cooldown: 2 }
        ]
    },
    arqueiro: {
        name: 'Arqueiro',
        baseHealth: 90,
        baseStrength: 12,
        baseDefense: 5,
        icon: 'arqueiro-icon',
        description: 'Combatente à distância com bom equilíbrio entre ataque e defesa.',
        abilities: [
            { name: 'Tiro Preciso', type: 'attack', multiplier: 1.6, cooldown: 1 },
            { name: 'Esquiva', type: 'defense', multiplier: 1.3, cooldown: 2 }
        ]
    }
};

// Utilitários para gestão de dados
const DataManager = {
    // Salvar um personagem
    saveCharacter: function(character) {
        const characters = this.getCharacters();
        
        // Se não tiver ID, gerar um novo
        if (!character.id) {
            character.id = Date.now().toString();
            character.createdAt = new Date().toISOString();
        }
        
        character.updatedAt = new Date().toISOString();
        
        // Adiciona ou atualiza o personagem
        const index = characters.findIndex(c => c.id === character.id);
        if (index !== -1) {
            characters[index] = character;
        } else {
            characters.push(character);
        }
        
        localStorage.setItem('characters', JSON.stringify(characters));
        return character;
    },
    
    // Obter todos os personagens
    getCharacters: function() {
        const characters = localStorage.getItem('characters');
        return characters ? JSON.parse(characters) : [];
    },
    
    // Obter um personagem específico
    getCharacter: function(id) {
        const characters = this.getCharacters();
        return characters.find(character => character.id === id);
    },
    
    // Deletar um personagem
    deleteCharacter: function(id) {
        let characters = this.getCharacters();
        characters = characters.filter(character => character.id !== id);
        localStorage.setItem('characters', JSON.stringify(characters));
    },
    
    // Salvar registro de batalha
    saveBattleRecord: function(record) {
        const battleHistory = this.getBattleHistory();
        
        // Adicionar ID e timestamp
        record.id = Date.now().toString();
        record.date = new Date().toISOString();
        
        battleHistory.unshift(record); // Adiciona no início para manter ordem cronológica inversa
        localStorage.setItem('battleHistory', JSON.stringify(battleHistory));
        return record;
    },
    
    // Obter histórico de batalhas
    getBattleHistory: function() {
        const history = localStorage.getItem('battleHistory');
        return history ? JSON.parse(history) : [];
    }
};

// Funções auxiliares
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Inicialização da página
document.addEventListener('DOMContentLoaded', function() {
    // Destacar item de navegação ativo
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.main-nav a');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (currentPage === linkPage || 
            (currentPage === '' && linkPage === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}); 