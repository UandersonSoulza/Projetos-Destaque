package controller;

import dao.UsuarioDAO;

public class LoginController {

    UsuarioDAO dao = new UsuarioDAO();

    public boolean autenticar(String usuario, String senha) {

        return dao.validarLogin(usuario, senha);
    }
}