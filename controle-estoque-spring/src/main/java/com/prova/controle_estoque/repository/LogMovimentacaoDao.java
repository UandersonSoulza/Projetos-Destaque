package com.prova.controle_estoque.repository;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

import com.prova.controle_estoque.model.LogMovimentacao;

public class LogMovimentacaoDao {

    public boolean save(LogMovimentacao log) {
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement("INSERT INTO movement_logs (product_id, product_name, action, quantity_changed, user_login, timestamp) VALUES (?, ?, ?, ?, ?, ?)") ) {
            if (log.getIdProduto() != null) {
                statement.setInt(1, log.getIdProduto());
            } else {
                statement.setNull(1, java.sql.Types.INTEGER);
            }
            statement.setString(2, log.getNomeProduto());
            statement.setString(3, log.getAcao());
            statement.setInt(4, log.getQuantidadeAlterada());
            statement.setString(5, log.getLoginUsuario());
            statement.setTimestamp(6, Timestamp.valueOf(log.getDataHora()));
            
            int result = statement.executeUpdate();
            return result > 0;
        } catch (Exception e) {
            throw new RuntimeException("Erro ao salvar log de movimentação", e);
        }
    }

    public List<LogMovimentacao> getAllLogs() {
        List<LogMovimentacao> logs = new ArrayList<>();
        String query = "SELECT id, product_id, product_name, action, quantity_changed, user_login, timestamp " +
                       "FROM movement_logs ORDER BY timestamp DESC";
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement(query);
             ResultSet resultSet = statement.executeQuery()) {
            while (resultSet.next()) {
                LogMovimentacao log = new LogMovimentacao();
                log.setId(resultSet.getInt("id"));
                log.setIdProduto(resultSet.getInt("product_id"));
                log.setNomeProduto(resultSet.getString("product_name"));
                log.setAcao(resultSet.getString("action"));
                log.setQuantidadeAlterada(resultSet.getInt("quantity_changed"));
                log.setLoginUsuario(resultSet.getString("user_login"));
                log.setDataHora(resultSet.getTimestamp("timestamp").toLocalDateTime());
                logs.add(log);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erro ao buscar logs de movimentação", e);
        }
        return logs;
    }

    public List<LogMovimentacao> getLogsByUser(String userLogin) {
        List<LogMovimentacao> logs = new ArrayList<>();
        String query = "SELECT id, product_id, product_name, action, quantity_changed, user_login, timestamp " +
                       "FROM movement_logs WHERE user_login = ? ORDER BY timestamp DESC";
        try (Connection connection = ConexaoBancoDados.getConnection();
             PreparedStatement statement = connection.prepareStatement(query)) {
            statement.setString(1, userLogin);
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    LogMovimentacao log = new LogMovimentacao();
                    log.setId(resultSet.getInt("id"));
                    log.setIdProduto(resultSet.getInt("product_id"));
                    log.setNomeProduto(resultSet.getString("product_name"));
                    log.setAcao(resultSet.getString("action"));
                    log.setQuantidadeAlterada(resultSet.getInt("quantity_changed"));
                    log.setLoginUsuario(resultSet.getString("user_login"));
                    log.setDataHora(resultSet.getTimestamp("timestamp").toLocalDateTime());
                    logs.add(log);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Erro ao buscar logs de movimentação do usuário", e);
        }
        return logs;
    }
}
