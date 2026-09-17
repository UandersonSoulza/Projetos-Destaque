package com.prova.controle_estoque.controller;

import com.prova.controle_estoque.model.Categoria;
import com.prova.controle_estoque.model.Produto;
import com.prova.controle_estoque.model.Usuario;
import com.prova.controle_estoque.repository.CategoriaDao;
import com.prova.controle_estoque.repository.LogMovimentacaoDao;
import com.prova.controle_estoque.repository.ProdutoDao;

import jakarta.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ControladorProduto {

    private final ProdutoDao produtoDao = new ProdutoDao();
    private final CategoriaDao categoriaDao = new CategoriaDao();
    private final LogMovimentacaoDao logMovimentacaoDao = new LogMovimentacaoDao();

    // Usado SOMENTE pela aplicação Desktop (Swing). Cada janela do Swing cria a
    // sua própria instância de ControladorProduto (veja TelaPrincipal), então não
    // há problema de concorrência aqui — é uma instância por usuário/processo,
    // e não um bean singleton compartilhado como no lado Web.
    private Usuario currentUser;

    public ControladorProduto() {
    }

    public ControladorProduto(Usuario currentUser) {
        this.currentUser = currentUser;
    }

    // ----- Páginas (views) -----

    @GetMapping("/produtos")
    public String produtos() {
        return "produtos";
    }

    @GetMapping("/categorias")
    public String categoriasPage() {
        return "categorias";
    }

    @GetMapping("/movimentos")
    public String movimentos() {
        return "movimentos";
    }

    // ----- Regras de negócio -----
    // Observação: o usuário logado é sempre obtido da HttpSession da requisição
    // atual, nunca de um campo de instância do controller. O Spring mantém os
    // controllers como singletons compartilhados por TODAS as requisições, então
    // guardar o usuário logado em um atributo da classe misturaria os dados de
    // usuários diferentes acessando o sistema ao mesmo tempo.

    private Usuario usuarioLogado(HttpSession session) {
        return (Usuario) session.getAttribute(ControladorAutenticacao.SESSION_ATTR);
    }

    public List<Produto> listAll() {
        return produtoDao.findAll();
    }

    public List<Categoria> listCategories() {
        return categoriaDao.findAll();
    }

    public List<Produto> searchByName(String name) {
        if (name == null || name.isBlank()) {
            return listAll();
        }
        return produtoDao.findByName(name.trim());
    }

    public Optional<String> addProduct(Usuario currentUser, String name, String quantityText, String priceText, Integer categoryId) {
        if (name == null || name.isBlank()) {
            return Optional.of("Nome do produto é obrigatório.");
        }
        int quantity;
        double price;
        try {
            quantity = Integer.parseInt(quantityText.trim());
            if (quantity < 0) {
                return Optional.of("Quantidade deve ser um número inteiro não negativo.");
            }
        } catch (NumberFormatException e) {
            return Optional.of("Quantidade deve ser um número inteiro válido.");
        }
        try {
            price = Double.parseDouble(priceText.trim());
            if (price < 0) {
                return Optional.of("Preço deve ser um número não negativo.");
            }
        } catch (NumberFormatException e) {
            return Optional.of("Preço deve ser um número válido.");
        }
        Produto produto = new Produto();
        produto.setName(name.trim());
        produto.setQuantity(quantity);
        produto.setPrice(price);
        produto.setUserId(currentUser.getId());
        produto.setCategoryId(categoryId);
        boolean saved = produtoDao.save(produto, currentUser.getLogin());
        return saved ? Optional.empty() : Optional.of("Erro ao cadastrar produto.");
    }

    public Optional<String> updateProduct(Usuario currentUser, int productId, String name, String quantityText, String priceText, Integer categoryId) {
        if (name == null || name.isBlank()) {
            return Optional.of("Nome do produto é obrigatório.");
        }
        Produto existing = produtoDao.findById(productId).orElse(null);
        if (existing == null) {
            return Optional.of("Produto não encontrado.");
        }
        int quantity;
        double price;
        try {
            quantity = Integer.parseInt(quantityText.trim());
            if (quantity < 0) {
                return Optional.of("Quantidade deve ser um número inteiro não negativo.");
            }
        } catch (NumberFormatException e) {
            return Optional.of("Quantidade deve ser um número inteiro válido.");
        }
        try {
            price = Double.parseDouble(priceText.trim());
            if (price < 0) {
                return Optional.of("Preço deve ser um número não negativo.");
            }
        } catch (NumberFormatException e) {
            return Optional.of("Preço deve ser um número válido.");
        }
        existing.setName(name.trim());
        existing.setQuantity(quantity);
        existing.setPrice(price);
        existing.setCategoryId(categoryId);
        boolean updated = produtoDao.update(existing, currentUser.getLogin());
        return updated ? Optional.empty() : Optional.of("Erro ao atualizar produto.");
    }

    public boolean deleteProduct(Usuario currentUser, int productId) {
        return produtoDao.delete(productId, currentUser.getLogin());
    }

    public Produto getProductById(int productId) {
        return produtoDao.findById(productId).orElse(null);
    }

    // ----- Sobrecargas usadas pela aplicação Desktop (Swing), que usam o
    // usuário definido no construtor em vez de recebê-lo por parâmetro. -----

    public Optional<String> addProduct(String name, String quantityText, String priceText, Integer categoryId) {
        return addProduct(currentUser, name, quantityText, priceText, categoryId);
    }

    public Optional<String> updateProduct(int productId, String name, String quantityText, String priceText, Integer categoryId) {
        return updateProduct(currentUser, productId, name, quantityText, priceText, categoryId);
    }

    public boolean deleteProduct(int productId) {
        return deleteProduct(currentUser, productId);
    }

    // ----- API REST -----

    @GetMapping("/api/produtos")
    @ResponseBody
    public ResponseEntity<?> apiListarProdutos(@RequestParam(required = false) String nome, HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return ResponseEntity.ok(searchByName(nome));
    }

    @GetMapping("/api/produtos/{id}")
    @ResponseBody
    public ResponseEntity<?> apiObterProduto(@PathVariable int id, HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        Produto produto = getProductById(id);
        return produto != null ? ResponseEntity.ok(produto) : ResponseEntity.notFound().build();
    }

    @PostMapping("/api/produtos")
    @ResponseBody
    public ResponseEntity<?> apiCriarProduto(@RequestBody Produto produto, HttpSession session) {
        Usuario usuario = usuarioLogado(session);
        if (usuario == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        Optional<String> erro = addProduct(usuario, produto.getName(), String.valueOf(produto.getQuantity()), String.valueOf(produto.getPrice()), produto.getCategoryId());
        return erro.isPresent()
                ? ResponseEntity.badRequest().body(Map.of("message", erro.get()))
                : ResponseEntity.status(201).body(Map.of("message", "Produto cadastrado com sucesso"));
    }

    @PutMapping("/api/produtos/{id}")
    @ResponseBody
    public ResponseEntity<?> apiAtualizarProduto(@PathVariable int id, @RequestBody Produto produto, HttpSession session) {
        Usuario usuario = usuarioLogado(session);
        if (usuario == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        Optional<String> erro = updateProduct(usuario, id, produto.getName(), String.valueOf(produto.getQuantity()), String.valueOf(produto.getPrice()), produto.getCategoryId());
        return erro.isPresent()
                ? ResponseEntity.badRequest().body(Map.of("message", erro.get()))
                : ResponseEntity.ok(Map.of("message", "Produto atualizado com sucesso"));
    }

    @DeleteMapping("/api/produtos/{id}")
    @ResponseBody
    public ResponseEntity<?> apiExcluirProduto(@PathVariable int id, HttpSession session) {
        Usuario usuario = usuarioLogado(session);
        if (usuario == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return deleteProduct(usuario, id)
                ? ResponseEntity.ok(Map.of("message", "Produto removido com sucesso"))
                : ResponseEntity.notFound().build();
    }

    // Histórico de movimentações (INSERT/UPDATE/DELETE) gerado pelo LogMovimentacaoDao,
    // o mesmo utilizado pela aplicação desktop (Swing) — mantém consistência entre as duas interfaces.
    @GetMapping("/api/logs")
    @ResponseBody
    public ResponseEntity<?> apiListarLogs(HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return ResponseEntity.ok(logMovimentacaoDao.getAllLogs());
    }
}
