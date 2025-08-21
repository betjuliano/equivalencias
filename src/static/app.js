// Global variables
let allEquivalencias = [];
let currentEditId = null;
let sortDirection = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadEquivalencias();
    checkAuth();
    
    // Setup search functionality
    document.getElementById('searchInput').addEventListener('input', filterTable);
    
    // Setup form submission
    document.getElementById('equivalenciaForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        login();
    });
});

// Modal functions
function showLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
    document.getElementById('loginModal').classList.add('flex');
}

function hideLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('loginModal').classList.remove('flex');
    document.getElementById('loginForm').reset();
}

// Authentication functions
async function checkAuth() {
    try {
        const response = await fetch('/api/check-auth');
        const data = await response.json();
        
        if (data.authenticated) {
            showAdminSection(data.username);
        }
    } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showAlert('Por favor, preencha todos os campos.', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Login realizado com sucesso!', 'success');
            showAdminSection(data.username);
            hideLoginModal();
        } else {
            showAlert(data.error || 'Erro no login', 'error');
        }
    } catch (error) {
        showAlert('Erro de conexão. Tente novamente.', 'error');
        console.error('Erro no login:', error);
    }
}

async function logout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        hideAdminSection();
        showAlert('Logout realizado com sucesso!', 'info');
    } catch (error) {
        console.error('Erro no logout:', error);
    }
}

function showAdminSection(username) {
    document.getElementById('adminSection').classList.remove('hidden');
    document.getElementById('adminUsername').textContent = username;
    loadAdminTable();
}

function hideAdminSection() {
    document.getElementById('adminSection').classList.add('hidden');
    clearForm();
}

// Data loading functions
async function loadEquivalencias() {
    showLoading(true);
    
    try {
        const response = await fetch('/api/equivalencias');
        const data = await response.json();
        
        if (response.ok) {
            allEquivalencias = data;
            displayEquivalencias(data);
        } else {
            showAlert('Erro ao carregar equivalências', 'error');
        }
    } catch (error) {
        showAlert('Erro de conexão ao carregar dados', 'error');
        console.error('Erro ao carregar equivalências:', error);
    } finally {
        showLoading(false);
    }
}

function displayEquivalencias(equivalencias) {
    const tbody = document.getElementById('equivalenciasTable');
    const noResults = document.getElementById('noResults');
    
    if (equivalencias.length === 0) {
        tbody.innerHTML = '';
        noResults.classList.remove('hidden');
        return;
    }
    
    noResults.classList.add('hidden');
    
    tbody.innerHTML = equivalencias.map(equiv => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-4 py-4 text-sm text-gray-900 font-medium">${equiv.disciplina_adm}</td>
            <td class="px-4 py-4 text-sm text-gray-600">${equiv.codigo_adm}</td>
            <td class="px-4 py-4 text-sm text-gray-600">${equiv.ch_adm}</td>
            <td class="px-4 py-4 text-sm text-gray-900 font-medium">${equiv.disciplina_equiv}</td>
            <td class="px-4 py-4 text-sm text-gray-600">${equiv.codigo_equiv}</td>
            <td class="px-4 py-4 text-sm text-gray-600">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${equiv.curso_equiv}
                </span>
            </td>
            <td class="px-4 py-4 text-sm text-gray-600">${equiv.ch_equiv}</td>
            <td class="px-4 py-4 text-sm text-gray-600 max-w-xs">
                <div title="${equiv.justificativa}" class="truncate">
                    ${equiv.justificativa.length > 100 ? 
                      equiv.justificativa.substring(0, 100) + '...' : 
                      equiv.justificativa}
                </div>
            </td>
        </tr>
    `).join('');
}

async function loadAdminTable() {
    try {
        const response = await fetch('/api/equivalencias');
        const data = await response.json();
        
        if (response.ok) {
            displayAdminTable(data);
        }
    } catch (error) {
        console.error('Erro ao carregar tabela admin:', error);
    }
}

function displayAdminTable(equivalencias) {
    const tbody = document.getElementById('adminTable');
    
    tbody.innerHTML = equivalencias.map(equiv => `
        <tr class="hover:bg-gray-50 transition-colors">
            <td class="px-4 py-3 text-sm text-gray-900 font-medium">${equiv.disciplina_adm}</td>
            <td class="px-4 py-3 text-sm text-gray-900 font-medium">${equiv.disciplina_equiv}</td>
            <td class="px-4 py-3 text-sm text-gray-600">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${equiv.curso_equiv}
                </span>
            </td>
            <td class="px-4 py-3 text-center">
                <div class="flex justify-center space-x-2">
                    <button onclick="editEquivalencia(${equiv.id})" 
                            class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-lg transition-colors transform hover:scale-105">
                        <i class="fas fa-edit text-sm"></i>
                    </button>
                    <button onclick="deleteEquivalencia(${equiv.id})" 
                            class="bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg transition-colors transform hover:scale-105">
                        <i class="fas fa-trash text-sm"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Form handling functions
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        disciplina_adm: document.getElementById('disciplina_adm').value,
        codigo_adm: document.getElementById('codigo_adm').value,
        ch_adm: document.getElementById('ch_adm').value,
        disciplina_equiv: document.getElementById('disciplina_equiv').value,
        codigo_equiv: document.getElementById('codigo_equiv').value,
        curso_equiv: document.getElementById('curso_equiv').value,
        ch_equiv: document.getElementById('ch_equiv').value,
        justificativa: document.getElementById('justificativa').value
    };
    
    try {
        let response;
        if (currentEditId) {
            response = await fetch(`/api/equivalencias/${currentEditId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        } else {
            response = await fetch('/api/equivalencias', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        }
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert(currentEditId ? 'Equivalência atualizada com sucesso!' : 'Equivalência criada com sucesso!', 'success');
            clearForm();
            loadEquivalencias();
            loadAdminTable();
        } else {
            showAlert(data.error || 'Erro ao salvar equivalência', 'error');
        }
    } catch (error) {
        showAlert('Erro de conexão ao salvar', 'error');
        console.error('Erro ao salvar:', error);
    }
}

function clearForm() {
    document.getElementById('equivalenciaForm').reset();
    currentEditId = null;
    document.getElementById('cancelEdit').classList.add('hidden');
}

function cancelEdit() {
    clearForm();
}

async function editEquivalencia(id) {
    try {
        const equiv = allEquivalencias.find(e => e.id === id);
        if (!equiv) return;
        
        document.getElementById('disciplina_adm').value = equiv.disciplina_adm;
        document.getElementById('codigo_adm').value = equiv.codigo_adm;
        document.getElementById('ch_adm').value = equiv.ch_adm;
        document.getElementById('disciplina_equiv').value = equiv.disciplina_equiv;
        document.getElementById('codigo_equiv').value = equiv.codigo_equiv;
        document.getElementById('curso_equiv').value = equiv.curso_equiv;
        document.getElementById('ch_equiv').value = equiv.ch_equiv;
        document.getElementById('justificativa').value = equiv.justificativa;
        
        currentEditId = id;
        document.getElementById('cancelEdit').classList.remove('hidden');
        
        // Scroll to form
        document.getElementById('equivalenciaForm').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Erro ao editar:', error);
    }
}

async function deleteEquivalencia(id) {
    if (!confirm('Tem certeza que deseja excluir esta equivalência?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/equivalencias/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Equivalência excluída com sucesso!', 'success');
            loadEquivalencias();
            loadAdminTable();
        } else {
            showAlert(data.error || 'Erro ao excluir equivalência', 'error');
        }
    } catch (error) {
        showAlert('Erro de conexão ao excluir', 'error');
        console.error('Erro ao excluir:', error);
    }
}

// Search and filter functions
function filterTable() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    if (!searchTerm) {
        displayEquivalencias(allEquivalencias);
        return;
    }
    
    const filtered = allEquivalencias.filter(equiv => 
        equiv.disciplina_adm.toLowerCase().includes(searchTerm) ||
        equiv.codigo_adm.toLowerCase().includes(searchTerm) ||
        equiv.disciplina_equiv.toLowerCase().includes(searchTerm) ||
        equiv.codigo_equiv.toLowerCase().includes(searchTerm) ||
        equiv.curso_equiv.toLowerCase().includes(searchTerm) ||
        equiv.justificativa.toLowerCase().includes(searchTerm)
    );
    
    displayEquivalencias(filtered);
}

// Sort table function
function sortTable(columnIndex) {
    const columns = ['disciplina_adm', 'codigo_adm', 'ch_adm', 'disciplina_equiv', 'codigo_equiv', 'curso_equiv', 'ch_equiv', 'justificativa'];
    const column = columns[columnIndex];
    
    if (!sortDirection[column]) {
        sortDirection[column] = 'asc';
    } else {
        sortDirection[column] = sortDirection[column] === 'asc' ? 'desc' : 'asc';
    }
    
    const sorted = [...allEquivalencias].sort((a, b) => {
        let aVal = a[column].toLowerCase();
        let bVal = b[column].toLowerCase();
        
        if (sortDirection[column] === 'asc') {
            return aVal.localeCompare(bVal);
        } else {
            return bVal.localeCompare(aVal);
        }
    });
    
    displayEquivalencias(sorted);
}

// Utility functions
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function showAlert(message, type) {
    // Color mapping for different alert types
    const colors = {
        'success': 'bg-green-100 border-green-400 text-green-700',
        'error': 'bg-red-100 border-red-400 text-red-700',
        'warning': 'bg-yellow-100 border-yellow-400 text-yellow-700',
        'info': 'bg-blue-100 border-blue-400 text-blue-700'
    };
    
    const icons = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    };
    
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 z-50 max-w-sm w-full ${colors[type]} border-l-4 p-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i class="${icons[type]} mr-3"></i>
            <div class="flex-1">
                <p class="font-medium">${message}</p>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-gray-400 hover:text-gray-600">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Animate in
    setTimeout(() => {
        alertDiv.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.add('translate-x-full');
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 300);
        }
    }, 5000);
}

