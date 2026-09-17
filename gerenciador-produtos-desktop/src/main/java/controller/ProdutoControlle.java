package controller;

import dao.ProdutoDAO;
import java.util.ArrayList;
import model.Produto;

public class ProdutoControlle {

    ProdutoDAO dao = new ProdutoDAO();

    public void salvarProduto(Produto p) {
        dao.adicionar(p);
    }

    public ArrayList<Produto> listarProdutos() {
        return dao.listar();
    }

    public void excluirProduto(int id) {
        dao.remover(id);
    }

    public Produto buscarProduto(int id) {
        return dao.pesquisar(id);
    }

    public void atualizarProduto(Produto p) {
        dao.alterar(p);
    }

    public Iterable<Produto> buscarPorNome(String nome) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }
}

