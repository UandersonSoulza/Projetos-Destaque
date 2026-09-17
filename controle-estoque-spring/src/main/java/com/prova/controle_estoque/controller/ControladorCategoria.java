package com.prova.controle_estoque.controller;

import com.prova.controle_estoque.model.Categoria;
import com.prova.controle_estoque.model.Usuario;
import com.prova.controle_estoque.repository.CategoriaDao;

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
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ControladorCategoria {
    private final CategoriaDao categoriaDao = new CategoriaDao();

    private Usuario usuarioLogado(HttpSession session) {
        return (Usuario) session.getAttribute(ControladorAutenticacao.SESSION_ATTR);
    }

    public List<Categoria> listAll() {
        return categoriaDao.findAll();
    }

    public Optional<String> addCategory(String name) {
        if (name == null || name.isBlank()) {
            return Optional.of("Nome da categoria é obrigatório.");
        }
        String trimmed = name.trim();
        if (categoriaDao.existsByName(trimmed)) {
            return Optional.of("Já existe uma categoria com esse nome.");
        }
        Categoria categoria = new Categoria();
        categoria.setName(trimmed);
        boolean saved = categoriaDao.save(categoria);
        return saved ? Optional.empty() : Optional.of("Erro ao cadastrar categoria.");
    }

    public boolean deleteCategory(int id) {
        return categoriaDao.deleteById(id);
    }

    @GetMapping("/api/categorias")
    @ResponseBody
    public ResponseEntity<?> apiListarCategorias(HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return ResponseEntity.ok(listAll());
    }

    @PostMapping("/api/categorias")
    @ResponseBody
    public ResponseEntity<?> apiCriarCategoria(@RequestBody Categoria categoria, HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        Optional<String> erro = addCategory(categoria.getName());
        return erro.isPresent()
                ? ResponseEntity.badRequest().body(Map.of("message", erro.get()))
                : ResponseEntity.status(201).body(Map.of("message", "Categoria cadastrada com sucesso"));
    }

    @DeleteMapping("/api/categorias/{id}")
    @ResponseBody
    public ResponseEntity<?> apiExcluirCategoria(@PathVariable int id, HttpSession session) {
        if (usuarioLogado(session) == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return deleteCategory(id)
                ? ResponseEntity.ok(Map.of("message", "Categoria removida com sucesso"))
                : ResponseEntity.notFound().build();
    }
}
