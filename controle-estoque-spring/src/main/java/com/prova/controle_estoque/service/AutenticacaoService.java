package com.prova.controle_estoque.service;

import java.util.Optional;

import com.prova.controle_estoque.model.Usuario;
import com.prova.controle_estoque.repository.UsuarioDao;

public class AutenticacaoService {
    private final UsuarioDao usuarioDao = new UsuarioDao();

    public Optional<Usuario> autenticar(String login, String password) {
        if (login == null || login.isBlank() || password == null || password.isBlank()) {
            throw new IllegalArgumentException("Login e senha são obrigatórios.");
        }
        return usuarioDao.authenticate(login, password);
    }

    public String cadastrar(String login, String password) {
        if (login == null || login.isBlank()) {
            return "Login não pode ficar em branco.";
        }
        if (password == null || password.isBlank()) {
            return "Senha não pode ficar em branco.";
        }
        if (usuarioDao.existsByLogin(login)) {
            return "Login já cadastrado. Escolha outro nome.";
        }
        Usuario usuario = new Usuario();
        usuario.setLogin(login.trim());
        usuario.setPassword(password);
        if (!usuarioDao.save(usuario)) {
            return "Falha ao cadastrar usuário.";
        }
        return null;
    }
}
