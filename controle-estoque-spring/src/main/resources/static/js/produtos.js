/**
 * produtos.js
 * CRUD completo de produtos (Listar, Adicionar, Editar, Excluir),
 * com vínculo à tabela de categorias, consumindo /api/produtos e /api/categorias.
 */

let categoriasCache = [];
let editandoId = null;

async function carregarCategoriasNoSelect() {
    categoriasCache = await apiFetch('/api/categorias');
    const select = document.getElementById('categoryId');
    const options = ['<option value="">Sem categoria</option>']
        .concat(categoriasCache.map(c => `<option value="${c.id}">${escapeHtml(c.name)}</option>`));
    select.innerHTML = options.join('');
}

function categoriaNome(categoryId) {
    const categoria = categoriasCache.find(c => c.id === categoryId);
    return categoria ? categoria.name : null;
}

function renderProdutos(produtos) {
    const tbody = document.getElementById('tbody-produtos');

    if (!produtos || produtos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state">Nenhum produto cadastrado ainda.</div></td></tr>`;
        return;
    }

    tbody.innerHTML = produtos.map(p => `
        <tr>
            <td>${p.id}</td>
            <td>${escapeHtml(p.name)}</td>
            <td>${p.categoryName ? `<span class="badge badge-success">${escapeHtml(p.categoryName)}</span>` : '<span class="badge badge-neutral">Sem categoria</span>'}</td>
            <td>${p.quantity}</td>
            <td>${formatMoney(p.price)}</td>
            <td>
                <div class="row-actions">
                    <button type="button" class="btn-icon" data-action="editar" data-id="${p.id}">Editar</button>
                    <button type="button" class="btn-icon danger" data-action="excluir" data-id="${p.id}" data-name="${escapeHtml(p.name)}">Excluir</button>
                </div>
            </td>
        </tr>
    `).join('');
}

async function carregarProdutos() {
    const nome = document.getElementById('busca-nome').value.trim();
    const url = nome ? `/api/produtos?nome=${encodeURIComponent(nome)}` : '/api/produtos';
    const produtos = await apiFetch(url);
    renderProdutos(produtos);
}

function abrirModal(titulo) {
    document.getElementById('modal-titulo').textContent = titulo;
    document.getElementById('modal-produto').classList.add('open');
}

function fecharModal() {
    document.getElementById('modal-produto').classList.remove('open');
    document.getElementById('form-produto').reset();
    document.getElementById('form-produto-message').style.display = 'none';
    editandoId = null;
}

function abrirModalNovoProduto() {
    editandoId = null;
    abrirModal('Novo Produto');
}

async function abrirModalEditarProduto(id) {
    const produto = await apiFetch(`/api/produtos/${id}`);
    editandoId = id;
    document.getElementById('name').value = produto.name;
    document.getElementById('quantity').value = produto.quantity;
    document.getElementById('price').value = produto.price;
    document.getElementById('categoryId').value = produto.categoryId || '';
    abrirModal('Editar Produto');
}

async function excluirProduto(id, nome) {
    if (!confirm(`Excluir o produto "${nome}"? Esta ação também será registrada no histórico de movimentação.`)) {
        return;
    }
    try {
        await apiFetch(`/api/produtos/${id}`, { method: 'DELETE' });
        showToast('Produto removido com sucesso.', 'success');
        await carregarProdutos();
    } catch (err) {
        showToast(err.message || 'Erro ao excluir produto.', 'error');
    }
}

function mostrarErroForm(mensagem) {
    const el = document.getElementById('form-produto-message');
    el.textContent = mensagem;
    el.style.display = 'block';
}

async function salvarProduto(event) {
    event.preventDefault();
    document.getElementById('form-produto-message').style.display = 'none';

    const payload = {
        name: document.getElementById('name').value.trim(),
        quantity: Number(document.getElementById('quantity').value),
        price: Number(document.getElementById('price').value),
        categoryId: document.getElementById('categoryId').value ? Number(document.getElementById('categoryId').value) : null,
    };

    const btn = document.getElementById('btn-salvar-produto');
    btn.disabled = true;
    try {
        if (editandoId) {
            await apiFetch(`/api/produtos/${editandoId}`, { method: 'PUT', body: payload });
            showToast('Produto atualizado com sucesso.', 'success');
        } else {
            await apiFetch('/api/produtos', { method: 'POST', body: payload });
            showToast('Produto cadastrado com sucesso.', 'success');
        }
        fecharModal();
        await carregarProdutos();
    } catch (err) {
        mostrarErroForm(err.message || 'Erro ao salvar produto.');
    } finally {
        btn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const user = await requireLogin();
    renderTopbar('produtos', user);

    await carregarCategoriasNoSelect();
    await carregarProdutos();

    document.getElementById('btn-novo-produto').addEventListener('click', abrirModalNovoProduto);
    document.getElementById('btn-fechar-modal').addEventListener('click', fecharModal);
    document.getElementById('btn-cancelar-modal').addEventListener('click', fecharModal);
    document.getElementById('form-produto').addEventListener('submit', salvarProduto);

    document.getElementById('btn-buscar').addEventListener('click', carregarProdutos);
    document.getElementById('busca-nome').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') { e.preventDefault(); carregarProdutos(); }
    });

    document.getElementById('tbody-produtos').addEventListener('click', (event) => {
        const btn = event.target.closest('button[data-action]');
        if (!btn) return;
        const id = Number(btn.dataset.id);
        if (btn.dataset.action === 'editar') {
            abrirModalEditarProduto(id);
        } else if (btn.dataset.action === 'excluir') {
            excluirProduto(id, btn.dataset.name);
        }
    });
});
