# Sistema de Gerenciamento de Consultas Médicas

Aplicação web full stack para gestão de uma clínica: cadastro de pacientes e médicos, agendamento de consultas, registro de exames e controle de usuários com autenticação e perfis de acesso.

## Tecnologias

- **Python 3** + **Flask** (back-end, sem ORM — SQL explícito via `mysql-connector-python`)
- **MySQL** (banco relacional)
- **HTML/CSS/JavaScript** (front-end server-side rendering com Jinja2)

## Funcionalidades

- Autenticação com senha criptografada (hash) e controle de sessão
- Perfis de acesso distintos (administrador / atendente)
- CRUD completo de **pacientes**, **médicos**, **consultas** e **exames**
- Regras de negócio no domínio: CPF e CRM únicos, impedir agendamento duplo de horário para o mesmo médico, impedir exclusão de registros com vínculos ativos, bloqueio de datas retroativas

## Arquitetura

```
sistema-consultas-medicas/
├── database/       # script de criação do schema e seed do admin inicial
├── models/         # regras de negócio e acesso a dados (sem ORM)
├── routes/         # blueprints Flask (auth + um por entidade)
├── static/         # CSS e JS
├── templates/      # views HTML (Jinja2)
├── app.py          # ponto de entrada
└── config.py       # configuração via variáveis de ambiente
```

## Como rodar

### Pré-requisitos
- Python 3.10+
- MySQL Server local

### Passos

```bash
# 1. Criar o banco
# execute o script database/schema.sql no seu MySQL

# 2. Configurar variáveis de ambiente
cp .env.example .env
# edite o .env com usuário/senha do seu MySQL local

# 3. Instalar dependências
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Criar o usuário administrador inicial
python -m database.seed_admin

# 5. Rodar a aplicação
python app.py
```

Acesse `http://127.0.0.1:5000` e faça login com o usuário administrador criado no passo anterior.

## Observações técnicas

O acesso a dados foi feito propositalmente sem ORM (SQLAlchemy), usando `mysql-connector-python` puro — decisão didática para deixar as queries SQL explícitas e visíveis.
