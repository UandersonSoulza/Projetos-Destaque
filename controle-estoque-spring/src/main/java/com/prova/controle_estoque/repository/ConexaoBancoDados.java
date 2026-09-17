package com.prova.controle_estoque.repository;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;

public class ConexaoBancoDados {
    // Classe responsável por abrir a conexão com o banco de dados e preparar as tabelas iniciais.

    private static final String DEFAULT_URL = "jdbc:mysql://localhost:3306/controle_estoque";
    private static final String DEFAULT_USERNAME = "root";
    private static final String DEFAULT_PASSWORD = "123123";

    // Método que lê as propriedades do arquivo de configuração da aplicação.
    private static Properties loadProperties() {
        Properties properties = new Properties();
        try (InputStream inputStream = ConexaoBancoDados.class.getClassLoader()
                .getResourceAsStream("application.properties")) {
            if (inputStream != null) {
                properties.load(inputStream);
            }
        } catch (IOException e) {
            throw new RuntimeException("Erro ao ler application.properties", e);
        }
        return properties;
    }

    // Método que resolve o valor de uma propriedade com fallback para o padrão.
    private static String getProperty(String key, String defaultValue) {
        String value = System.getProperty(key);
        if (value != null && !value.isBlank()) {
            return value;
        }
        Properties properties = loadProperties();
        value = properties.getProperty(key);
        return (value != null && !value.isBlank()) ? value : defaultValue;
    }

    // Método que cria a conexão com o banco de dados.
    public static Connection getConnection() throws SQLException {
        String url = getProperty("spring.datasource.url", DEFAULT_URL);
        String username = getProperty("spring.datasource.username", DEFAULT_USERNAME);
        String password = getProperty("spring.datasource.password", DEFAULT_PASSWORD);

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            throw new SQLException("Driver JDBC do MySQL não encontrado", e);
        }

        return DriverManager.getConnection(url, username, password);
    }

    // Método que inicializa as tabelas principais do sistema.
    public static void initializeDatabase() throws SQLException {
        try (Connection connection = getConnection(); Statement statement = connection.createStatement()) {
            statement.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        login VARCHAR(100) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL
                    )
                    """);

            statement.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE
                    )
                    """);

            statement.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        quantity INT NOT NULL DEFAULT 0,
                        price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                        user_id INT NOT NULL,
                        category_id INT NULL,
                        CONSTRAINT fk_products_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                    )
                    """);

            statement.executeUpdate("""
                    CREATE TABLE IF NOT EXISTS movement_logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        product_id INT NULL,                        product_name VARCHAR(255) NOT NULL,
                        action VARCHAR(20) NOT NULL,
                        quantity_changed INT NOT NULL,
                        user_login VARCHAR(100) NOT NULL,
                        timestamp DATETIME NOT NULL
                    )
                    """);
        }
    }
}
