// Sistema de Gerenciamento de Consultas Medicas
// Pequenos utilitarios de interface (sem dependencias externas)

document.addEventListener("DOMContentLoaded", function () {
  // Confirmacao antes de acoes destrutivas (excluir / cancelar)
  document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
    form.addEventListener("submit", function (evento) {
      const mensagem = form.getAttribute("data-confirmar") || "Tem certeza?";
      if (!window.confirm(mensagem)) {
        evento.preventDefault();
      }
    });
  });

  // Fecha os alertas (flash messages) automaticamente apos alguns segundos
  document.querySelectorAll(".flash").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity .4s ease";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 400);
    }, 5000);
  });

  // Preenche o formulario de edicao com os dados da linha clicada (data-editar)
  document.querySelectorAll("[data-editar]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      const alvoSeletor = botao.getAttribute("data-editar");
      const painel = document.querySelector(alvoSeletor);
      if (!painel) return;

      painel.open = true;
      const dados = JSON.parse(botao.getAttribute("data-valores") || "{}");
      Object.keys(dados).forEach(function (campo) {
        const input = painel.querySelector('[name="' + campo + '"]');
        if (input) input.value = dados[campo];
      });

      const acaoForm = botao.getAttribute("data-acao");
      const form = painel.querySelector("form.form-editavel");
      if (form && acaoForm) form.setAttribute("action", acaoForm);

      painel.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
