package dao;

import model.Usuario;

public class UsuarioDAO {

    private Usuario usuario = new Usuario("admin", "123");

    public boolean validarLogin(String user, String senha) {

        return usuario.getUsuario().equals(user)
                && usuario.getSenha().equals(senha);
    }
}