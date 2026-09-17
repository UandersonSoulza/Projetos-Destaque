package com.prova.controle_estoque;

import com.prova.controle_estoque.repository.ConexaoBancoDados;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ControleEstoqueApplication {

    public static void main(String[] args) {
        try {
            ConexaoBancoDados.initializeDatabase();
        } catch (Exception e) {
            System.err.println("Banco não disponível no momento: " + e.getMessage());
        }
        SpringApplication.run(ControleEstoqueApplication.class, args);
    }
}
