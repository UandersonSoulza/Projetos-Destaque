/**
 * categorias.js
 * Listagem, cadastro e exclusão de categorias, consumindo /api/categorias.
 */

function renderCategorias(categorias) {
    const tbody = document.getElementById('tbody-categorias');

    if (!categorias || categorias.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3"><div class="empty-state">Nenhuma categoria cadastrada ainda.</div></td></tr>`;
        return;
    }

    tbody.innerHTML = categorias.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${escapeHtml(c.name)}</td>
            <td>
                <div class="row-actions">
                    <button type="button" class="btn-icon danger" data-action="excluir" data-id="${c.id}" data-name="${escapeHtml(c.name)}">Excluir</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function carregarCategorias() {
    const categorias = await apiFetch('/api/categorias');
    renderCategorias(categorias);
}

function abrirModal() {
    document.getElementById('modal-categoria').classList.add('open');
}

function fecharModal() {
    document.getElementById('modal-categoria').classList.remove('open');
    document.getElementById('form-categoria').reset();
    document.getElementById('form-categoria-message').style.display = 'none';
}

async function excluirCategoria(id, nome) {
    if (!confirm(`Excluir a categoria "${nome}"? Produtos vinculados ficarão sem categoria.`)) {
        return;
    }
    try {
        await apiFetch(`/api/categorias/${id}`, { method: 'DELETE' });
        showToast('Categoria removida com sucesso.', 'success');
        await carregarCategorias();
    } catch (err) {
        showToast(err.message || 'Erro ao excluir categoria.', 'error');
    }
}

async function salvarCategoria(event) {
    event.preventDefault();
    const msgEl = document.getElementById('form-categoria-message');
    msgEl.style.display = 'none';

    const name = document.getElementById('categoria-name').value.trim();
    const btn = document.getElementById('btn-salvar-categoria');

    btn.disabled = true;
    try {
        await apiFetch('/api/categorias', { method: 'POST', body: { name } });
        showToast('Categoria cadastrada com sucesso.', 'success');
        fecharModal();
        await carregarCategorias();
    } catch (err) {
        msgEl.textContent = err.message || 'Erro ao cadastrar categoria.';
        msgEl.style.display = 'block';
    } finally {
        btn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const user = await requireLogin();
    renderTopbar('categorias', user);

    await carregarCategorias();

    document.getElementById('btn-nova-categoria').addEventListener('click', abrirModal);
    document.getElementById('btn-fechar-modal').addEventListener('click', fecharModal);
    document.getElementById('btn-cancelar-modal').addEventListener('click', fecharModal);
    document.getElementById('form-categoria').addEventListener('submit', salvarCategoria);

    document.getElementById('tbody-categorias').addEventListener('click', (event) => {
        const btn = event.target.closest('button[data-action="excluir"]');
        if (!btn) return;
        excluirCategoria(Number(btn.dataset.id), btn.dataset.name);
    });
});
