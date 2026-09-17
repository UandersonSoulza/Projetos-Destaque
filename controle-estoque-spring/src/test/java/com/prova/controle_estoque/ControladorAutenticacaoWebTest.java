package com.prova.controle_estoque;

import com.prova.controle_estoque.controller.ControladorAutenticacao;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ControladorAutenticacaoWebTest {

    @Test
    void loginRouteShouldReturnLoginView() {
        ControladorAutenticacao controller = new ControladorAutenticacao();
        assertEquals("login", controller.login());
    }
}
