/**
 * common.js
 * Funções compartilhadas entre todas as páginas do sistema web.
 * Toda comunicação com o back-end (Spring @RestController) é feita
 * via fetch API, em JSON, sem reload de página.
 */

/**
 * Wrapper de fetch que já envia/recebe JSON e credenciais de sessão
 * (cookie JSESSIONID), e lança um erro com a mensagem vinda do back-end
 * quando a resposta não é 2xx.
 */
async function apiFetch(url, options = {}) {
    const opts = {
        method: options.method || 'GET',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    };
    if (options.body !== undefined) {
        opts.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, opts);

    let data = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
        data = await response.json().catch(() => null);
    }

    if (!response.ok) {
        const message = (data && (data.message || data)) || `Erro na requisição (HTTP ${response.status})`;
        const error = new Error(typeof message === 'string' ? message : JSON.stringify(message));
        error.status = response.status;
        error.data = data;
        throw error;
    }

    return data;
}

/** Escapa texto antes de inserir em innerHTML, evitando quebra de layout/HTML injection. */
function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/** Formata um número como moeda brasileira (R$). */
function formatMoney(value) {
    const number = Number(value) || 0;
    return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

/** Formata um timestamp ISO (ou similar) no padrão dd/mm/aaaa hh:mm. */
function formatDateTime(value) {
    if (!value) return '-';
    const date = new Date(value);
    if (isNaN(date.getTime())) return String(value);
    return date.toLocaleString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}

/**
 * Exibe uma notificação temporária (toast) no canto da tela.
 * type: 'success' | 'error' | 'info' (padrão)
 */
function showToast(message, type = 'info') {
    let toast = document.getElementById('app-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'app-toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.className = 'toast show' + (type === 'error' ? ' toast-error' : type === 'success' ? ' toast-success' : '');
    toast.textContent = message;

    clearTimeout(toast._hideTimeout);
    toast._hideTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3500);
}

/**
 * Garante que existe um usuário autenticado (via GET /api/session).
 * Caso contrário, redireciona para a tela de login.
 * Retorna os dados do usuário logado ({ id, login }) em caso de sucesso.
 */
async function requireLogin() {
    try {
        return await apiFetch('/api/session');
    } catch (err) {
        window.location.href = '/login';
        // interrompe a execução do script chamador
        throw err;
    }
}

/** Efetua logout e redireciona para a tela de login. */
async function logout() {
    try {
        await apiFetch('/api/logout', { method: 'POST' });
    } finally {
        window.location.href = '/login';
    }
}

/**
 * Renderiza a barra de navegação superior (topbar) dentro do elemento #topbar.
 * activePage: 'produtos' | 'categorias' | 'movimentos'
 */
function renderTopbar(activePage, user) {
    const el = document.getElementById('topbar');
    if (!el) return;

    const links = [
        { href: '/produtos', label: 'Produtos', key: 'produtos' },
        { href: '/categorias', label: 'Categorias', key: 'categorias' },
        { href: '/movimentos', label: 'Histórico', key: 'movimentos' },
    ];

    const navHtml = links.map(link =>
        `<a href="${link.href}" class="${link.key === activePage ? 'active' : ''}">${link.label}</a>`
    ).join('');

    el.innerHTML = `
        <div class="topbar-brand">Controle de Estoque</div>
        <nav class="topbar-nav">${navHtml}</nav>
        <div class="topbar-user">
            <span>Usuário: <strong>${escapeHtml(user ? user.login : '')}</strong></span>
            <button type="button" class="btn btn-secondary" id="btn-logout">Sair</button>
        </div>
    `;

    document.getElementById('btn-logout').addEventListener('click', logout);
}
