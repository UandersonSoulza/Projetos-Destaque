package dao;

import java.util.ArrayList;
import model.Produto;

public class ProdutoDAO {

    private ArrayList<Produto> listaProdutos = new ArrayList<>();

    public void adicionar(Produto p) {
        listaProdutos.add(p);
    }

    public ArrayList<Produto> listar() {
        return listaProdutos;
    }

    public void remover(int id) {
        Produto produtoRemover = null;
        for (Produto p : listaProdutos) {
            if (p.getId() == id) {
                produtoRemover = p;
            }
        }
        listaProdutos.remove(produtoRemover);
    }

    public Produto pesquisar(int id) {
        for (Produto p : listaProdutos) {
            if (p.getId() == id) return p;
        }
        return null;
    }

    public void alterar(Produto produtoAtualizado) {
        for (Produto p : listaProdutos) {
            if (p.getId() == produtoAtualizado.getId()) {
                p.setNome(produtoAtualizado.getNome());
                p.setCategoria(produtoAtualizado.getCategoria());
                p.setPreco(produtoAtualizado.getPreco());
                p.setQuantidade(produtoAtualizado.getQuantidade());
            }
        }
    }
}

