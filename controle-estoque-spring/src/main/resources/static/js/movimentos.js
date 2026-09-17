/**
 * movimentos.js
 * Exibe o histórico de movimentações (INSERT/UPDATE/DELETE) gerado
 * automaticamente pelo LogMovimentacaoDao a cada operação de produto,
 * tanto pela interface Web quanto pela aplicação Desktop (Swing).
 */

const BADGE_POR_ACAO = {
    INSERT: { classe: 'badge-success', label: 'Entrada' },
    UPDATE: { classe: 'badge-warning', label: 'Atualização' },
    DELETE: { classe: 'badge-danger', label: 'Saída' },
};

function badgeAcao(acao) {
    const info = BADGE_POR_ACAO[acao] || { classe: 'badge-neutral', label: acao };
    return `<span class="badge ${info.classe}">${escapeHtml(info.label)}</span>`;
}

function renderLogs(logs) {
    const tbody = document.getElementById('tbody-logs');

    if (!logs || logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5"><div class="empty-state">Nenhuma movimentação registrada ainda.</div></td></tr>`;
        return;
    }

    tbody.innerHTML = logs.map(log => `
        <tr>
            <td>${formatDateTime(log.dataHora)}</td>
            <td>${escapeHtml(log.nomeProduto)}</td>
            <td>${badgeAcao(log.acao)}</td>
            <td>${log.quantidadeAlterada}</td>
            <td>${escapeHtml(log.loginUsuario)}</td>
        </tr>
    `).join('');
}

async function carregarLogs() {
    const logs = await apiFetch('/api/logs');
    renderLogs(logs);
}

document.addEventListener('DOMContentLoaded', async () => {
    const user = await requireLogin();
    renderTopbar('movimentos', user);
    await carregarLogs();

    document.getElementById('btn-atualizar').addEventListener('click', carregarLogs);
});
