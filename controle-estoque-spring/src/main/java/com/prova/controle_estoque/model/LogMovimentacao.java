package com.prova.controle_estoque.model;

import java.time.LocalDateTime;

public class LogMovimentacao {
    private int id;
    private Integer idProduto;
    private String nomeProduto;
    private String acao; // INSERT, UPDATE, DELETE
    private int quantidadeAlterada;
    private String loginUsuario;
    private LocalDateTime dataHora;

    public LogMovimentacao() {}

    public LogMovimentacao(Integer idProduto, String nomeProduto, String acao, int quantidadeAlterada, String loginUsuario) {
        this.idProduto = idProduto;
        this.nomeProduto = nomeProduto;
        this.acao = acao;
        this.quantidadeAlterada = quantidadeAlterada;
        this.loginUsuario = loginUsuario;
        this.dataHora = LocalDateTime.now();
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Integer getIdProduto() {
        return idProduto;
    }

    public void setIdProduto(Integer idProduto) {
        this.idProduto = idProduto;
    }

    public String getNomeProduto() {
        return nomeProduto;
    }

    public void setNomeProduto(String nomeProduto) {
        this.nomeProduto = nomeProduto;
    }

    public String getAcao() {
        return acao;
    }

    public void setAcao(String acao) {
        this.acao = acao;
    }

    public int getQuantidadeAlterada() {
        return quantidadeAlterada;
    }

    public void setQuantidadeAlterada(int quantidadeAlterada) {
        this.quantidadeAlterada = quantidadeAlterada;
    }

    public String getLoginUsuario() {
        return loginUsuario;
    }

    public void setLoginUsuario(String loginUsuario) {
        this.loginUsuario = loginUsuario;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public void setDataHora(LocalDateTime dataHora) {
        this.dataHora = dataHora;
    }
}
