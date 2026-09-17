package com.prova.controle_estoque.controller;

import com.prova.controle_estoque.model.Usuario;
import com.prova.controle_estoque.service.AutenticacaoService;
import jakarta.servlet.http.HttpSession;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ControladorAutenticacao {

    public static final String SESSION_ATTR = "usuarioLogado";

    private final AutenticacaoService autenticacaoService = new AutenticacaoService();

    @GetMapping("/")
    public String index() {
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    @PostMapping("/login")
    public String autenticar(@RequestParam String login, @RequestParam String password, Model model) {
        try {
            Optional<Usuario> usuario = login(login, password);
            if (usuario.isPresent()) {
                return "redirect:/produtos";
            }
            model.addAttribute("message", "Login ou senha inválidos.");
            return "login";
        } catch (IllegalArgumentException e) {
            model.addAttribute("message", e.getMessage());
            return "login";
        }
    }

    @GetMapping("/register")
    public String registerPage() {
        return "cadastro";
    }

    @PostMapping("/register")
    public String registrar(@RequestParam String login, @RequestParam String password, Model model) {
        String resultado = register(login, password);
        if (resultado == null) {
            return "redirect:/login";
        }
        model.addAttribute("message", resultado);
        return "cadastro";
    }

    public Optional<Usuario> login(String login, String password) {
        return autenticacaoService.autenticar(login, password);
    }

    public String register(String login, String password) {
        return autenticacaoService.cadastrar(login, password);
    }

    // ==========================================================
    // API REST (usada pelo front-end via fetch, sem reload de página)
    // ==========================================================

    private Map<String, Object> usuarioSeguro(Usuario usuario) {
        Map<String, Object> dados = new LinkedHashMap<>();
        dados.put("id", usuario.getId());
        dados.put("login", usuario.getLogin());
        return dados;
    }

    @PostMapping("/api/login")
    @ResponseBody
    public ResponseEntity<?> apiLogin(@RequestBody Usuario usuario, HttpSession session) {
        try {
            Optional<Usuario> autenticado = autenticacaoService.autenticar(usuario.getLogin(), usuario.getPassword());
            if (autenticado.isPresent()) {
                // Guarda o usuário autenticado na sessão HTTP (por navegador/aba),
                // evitando o uso de campos de instância no controller (que seria
                // compartilhado entre TODOS os usuários simultâneos da aplicação).
                session.setAttribute(SESSION_ATTR, autenticado.get());
                return ResponseEntity.ok(usuarioSeguro(autenticado.get()));
            }
            return ResponseEntity.status(401).body(Map.of("message", "Login ou senha inválidos"));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("message", e.getMessage()));
        }
    }

    @PostMapping("/api/logout")
    @ResponseBody
    public ResponseEntity<?> apiLogout(HttpSession session) {
        session.invalidate();
        return ResponseEntity.ok(Map.of("message", "Sessão finalizada"));
    }

    @GetMapping("/api/session")
    @ResponseBody
    public ResponseEntity<?> apiSessao(HttpSession session) {
        Usuario usuario = (Usuario) session.getAttribute(SESSION_ATTR);
        if (usuario == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Não autenticado"));
        }
        return ResponseEntity.ok(usuarioSeguro(usuario));
    }

    @PostMapping("/api/usuarios")
    @ResponseBody
    public ResponseEntity<?> apiCadastrarUsuario(@RequestBody Usuario usuario) {
        String resultado = autenticacaoService.cadastrar(usuario.getLogin(), usuario.getPassword());
        return resultado == null
                ? ResponseEntity.status(201).body(Map.of("message", "Usuário cadastrado com sucesso"))
                : ResponseEntity.badRequest().body(Map.of("message", resultado));
    }
}
