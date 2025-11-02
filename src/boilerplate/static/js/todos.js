// Variáveis globais
let currentTodoId = null;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    setupEventListeners();
});

// Configura os event listeners
function setupEventListeners() {
    // Filtro de busca
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(loadTodos, 300));
    }

    // Filtro de status
    const filterSelect = document.getElementById('filter');
    if (filterSelect) {
        filterSelect.addEventListener('change', loadTodos);
    }
}

// Carrega as tarefas da API
async function loadTodos() {
    const search = document.getElementById('search')?.value || '';
    const filter = document.getElementById('filter')?.value || 'all';
    
    try {
        const response = await fetch(`/api/v1/todos?search=${encodeURIComponent(search)}&filter=${filter}`);
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        showToast('Erro ao carregar tarefas', 'error');
    }
}

// Renderiza a lista de tarefas
function renderTodos(todos) {
    const container = document.getElementById('todos-container');
    if (!container) return;

    if (!todos || todos.length === 0) {
        container.innerHTML = `
            <div class="p-8 text-center bg-white rounded-lg shadow">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhuma tarefa encontrada</h3>
                <p class="mt-1 text-sm text-gray-500">Comece criando uma nova tarefa.</p>
                <div class="mt-6">
                    <button type="button" onclick="openCreateModal()" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
                        </svg>
                        Nova Tarefa
                    </button>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = todos.map(todo => `
        <div class="bg-white rounded-lg shadow p-4" id="todo-${todo.id}">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <div class="flex items-center">
                        <input 
                            type="checkbox" 
                            ${todo.completed ? 'checked' : ''} 
                            onchange="toggleTodoStatus(${todo.id}, this.checked)"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 cursor-pointer"
                        >
                        <h3 class="ml-3 text-lg font-medium text-gray-900 ${todo.completed ? 'line-through text-gray-500' : ''}">${escapeHtml(todo.title)}</h3>
                    </div>
                    ${todo.description ? `<p class="mt-2 text-sm text-gray-600">${escapeHtml(todo.description)}</p>` : ''}
                    <div class="mt-2 text-xs text-gray-500">
                        Criado em: ${new Date(todo.created_at).toLocaleString()}
                    </div>
                </div>
                <div class="flex space-x-2">
                    <button onclick="editTodo(${todo.id}, '${escapeHtml(todo.title)}', '${escapeHtml(todo.description || '')}', ${todo.completed})" 
                            class="p-2 text-gray-500 hover:text-blue-600 focus:outline-none">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                        </svg>
                    </button>
                    <button onclick="confirmDelete(${todo.id})" 
                            class="p-2 text-gray-500 hover:text-red-600 focus:outline-none">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Abre o modal para criar/editar uma tarefa
function openCreateModal(todo = null) {
    const modal = document.getElementById('todo-modal');
    const title = document.getElementById('modal-title');
    const form = document.getElementById('todo-form');
    
    if (todo) {
        title.textContent = 'Editar Tarefa';
        document.getElementById('todo-id').value = todo.id;
        document.getElementById('title').value = todo.title;
        document.getElementById('description').value = todo.description || '';
        document.getElementById('completed').checked = todo.completed;
    } else {
        title.textContent = 'Nova Tarefa';
        form.reset();
        document.getElementById('todo-id').value = '';
    }
    
    // Adiciona a classe active para ativar a animação e mostrar o modal
    modal.classList.remove('hidden');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Impede rolagem da página
    modal.setAttribute('aria-hidden', 'false');
}

// Fecha o modal
function closeModal() {
    const modal = document.getElementById('todo-modal');
    // Remove a classe active para iniciar a animação de saída
    modal.classList.remove('active');
    
    // Aguarda o término da animação antes de esconder o modal
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Restaura a rolagem da página
    }, 300); // Tempo igual à duração da transição no CSS (0.3s)
    
    modal.setAttribute('aria-hidden', 'true');
}

// Salva uma tarefa (cria ou atualiza)
async function saveTodo() {
    const id = document.getElementById('todo-id').value;
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const completed = document.getElementById('completed').checked;
    
    if (!title) {
        showToast('O título é obrigatório', 'error');
        return;
    }
    
    const todoData = {
        title,
        description: description || null,
        completed
    };
    
    try {
        const url = id ? `/api/v1/todos/${id}` : '/api/v1/todos/';
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(todoData)
        });
        
        if (!response.ok) throw new Error('Erro ao salvar a tarefa');
        
        closeModal();
        loadTodos();
        showToast(`Tarefa ${id ? 'atualizada' : 'criada'} com sucesso!`, 'success');
    } catch (error) {
        console.error('Erro ao salvar tarefa:', error);
        showToast('Erro ao salvar a tarefa', 'error');
    }
}

// Alterna o status de conclusão de uma tarefa
async function toggleTodoStatus(id, completed) {
    try {
        const response = await fetch(`/api/v1/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed })
        });
        
        if (!response.ok) throw new Error('Erro ao atualizar o status da tarefa');
        
        loadTodos();
        showToast('Status da tarefa atualizado', 'success');
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
        showToast('Erro ao atualizar o status da tarefa', 'error');
        loadTodos(); // Recarrega para manter a consistência
    }
}

// Abre o modal de confirmação para exclusão
function confirmDelete(id) {
    currentTodoId = id;
    const modal = document.getElementById('confirm-modal');
    modal.classList.remove('hidden');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Impede rolagem da página
    modal.setAttribute('aria-hidden', 'false');
}

// Fecha o modal de confirmação
function closeConfirmModal() {
    const modal = document.getElementById('confirm-modal');
    // Remove a classe active para iniciar a animação de saída
    modal.classList.remove('active');
    
    // Aguarda o término da animação antes de esconder o modal
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Restaura a rolagem da página
    }, 300); // Tempo igual à duração da transição no CSS (0.3s)
    
    modal.setAttribute('aria-hidden', 'true');
    currentTodoId = null;
}

// Exclui uma tarefa
async function deleteTodo() {
    if (!currentTodoId) return;
    
    try {
        const response = await fetch(`/api/v1/todos/${currentTodoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao excluir a tarefa');
        
        closeConfirmModal();
        loadTodos();
        showToast('Tarefa excluída com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao excluir tarefa:', error);
        showToast('Erro ao excluir a tarefa', 'error');
    }
}

// Preenche o formulário para edição
function editTodo(id, title, description, completed) {
    openCreateModal({ id, title, description, completed });
}

// Exibe uma mensagem de notificação
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg text-white ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    }`;
    
    toast.innerHTML = `
        <div class="flex items-center">
            <span>${message}</span>
            <button type="button" class="ml-4 text-white" onclick="this.parentElement.parentElement.remove()">
                <span class="sr-only">Fechar</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Remove a notificação após 5 segundos
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Função auxiliar para debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para escapar HTML e prevenir XSS
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Exporta as funções para o escopo global
window.openCreateModal = openCreateModal;
window.closeModal = closeModal;
window.saveTodo = saveTodo;
window.toggleTodoStatus = toggleTodoStatus;
window.confirmDelete = confirmDelete;
window.closeConfirmModal = closeConfirmModal;
window.deleteTodo = deleteTodo;
window.editTodo = editTodo;
