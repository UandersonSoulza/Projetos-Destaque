package com.prova.controle_estoque.repository;

import com.prova.controle_estoque.model.Movimento;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class MovimentacaoDao {

    public List<Movimento> getAllMovements() {
        List<Movimento> movimentos = new ArrayList<>();
        String query = "SELECT p.id, p.name, p.quantity, p.price, (p.quantity * p.price) AS total_value, u.login " +
                       "FROM products p " +
                       "JOIN users u ON p.user_id = u.id " +
                       "ORDER BY p.id";
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement(query);
             ResultSet resultSet = statement.executeQuery()) {
            while (resultSet.next()) {
                Movimento movimento = new Movimento();
                movimento.setIdProduto(resultSet.getInt("id"));
                movimento.setNomeProduto(resultSet.getString("name"));
                movimento.setQuantidade(resultSet.getInt("quantity"));
                movimento.setPreco(resultSet.getDouble("price"));
                movimento.setValorTotal(resultSet.getDouble("total_value"));
                movimento.setLoginUsuario(resultSet.getString("login"));
                movimentos.add(movimento);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erro ao buscar movimentações", e);
        }
        return movimentos;
    }

    public List<Movimento> getMovementsByUser(String userLogin) {
        List<Movimento> movimentos = new ArrayList<>();
        String query = "SELECT p.id, p.name, p.quantity, p.price, (p.quantity * p.price) AS total_value, u.login " +
                       "FROM products p " +
                       "JOIN users u ON p.user_id = u.id " +
                       "WHERE u.login = ? " +
                       "ORDER BY p.id";
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement(query)) {
            statement.setString(1, userLogin);
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    Movimento movimento = new Movimento();
                    movimento.setIdProduto(resultSet.getInt("id"));
                    movimento.setNomeProduto(resultSet.getString("name"));
                    movimento.setQuantidade(resultSet.getInt("quantity"));
                    movimento.setPreco(resultSet.getDouble("price"));
                    movimento.setValorTotal(resultSet.getDouble("total_value"));
                    movimento.setLoginUsuario(resultSet.getString("login"));
                    movimentos.add(movimento);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Erro ao buscar movimentações do usuário", e);
        }
        return movimentos;
    }

    public double getTotalInventoryValue() {
        String query = "SELECT SUM(p.quantity * p.price) AS total FROM products p";
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement(query);
             ResultSet resultSet = statement.executeQuery()) {
            if (resultSet.next()) {
                return resultSet.getDouble("total");
            }
        } catch (Exception e) {
            throw new RuntimeException("Erro ao calcular valor total do estoque", e);
        }
        return 0.0;
    }
}
