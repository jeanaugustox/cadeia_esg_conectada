# 🌐 Cadeia ESG Conectada

Projeto acadêmico desenvolvido em equipe no curso de Sistemas de Informação (CESAR School)

---

## 🎯 Objetivo

Desenvolver um sistema em Python para cadastro e gestão de empresas, usuários e certificados ESG, com foco em conectar marcas e fornecedores alinhados a práticas responsáveis.

## 🧩 Escopo atual

O sistema é um aplicativo de linha de comando (CLI) que permite:

- Cadastro, listagem, busca, edição e exclusão lógica de **empresas**  
- Cadastro, listagem, edição e exclusão lógica de **usuários**  
- **Autenticação** via login e recuperação de senha  
- Registro de **certificados ESG** associados às empresas  
- Geração de um **ranking de empresas por quantidade de certificados ESG**

Os dados são armazenados em arquivos **JSON** dentro da pasta `data/`.

## 🗂️ Estrutura do repositório

```txt
cadeia_esg_conectada/
├── src/
│   ├── app.py            # Menu principal e orquestração dos módulos
│   ├── empresas.py       # CRUD de empresas
│   ├── usuarios.py       # CRUD de usuários e papéis (Admin/Editor/Leitor)
│   ├── auth.py           # Autenticação, login e recuperação de senha
│   └── certificados.py   # Registro de certificados e ranking ESG
├── data/
│   ├── empresas.json     # Base de empresas cadastradas
│   └── usuarios.json     # Base de usuários cadastrados
└── README.md
````

## ⚙️ Tecnologias utilizadas

- 🐍 Python 3.x
- 📁 Armazenamento em arquivos JSON (data/empresas.json e data/usuarios.json)
- Sem dependências externas (apenas biblioteca padrão do Python)

## 🚀 Como executar o projeto

1. Clonar o repositório
   
```bash
git clone https://github.com/jeanaugustox/cadeia_esg_conectada.git
cd cadeia_esg_conectada
```
2. Executar o sistema

```bash
cd src
python app.py 
```

O menu principal será exibido no terminal com as opções de:

- Gerenciar Empresas
- Gerenciar Usuários
- Gerenciar Certificados
- Autenticação

## 1. Gestão de usuários (usuarios.py)

Cadastrar usuário com:
- nome
- email
- senha
- papel (Admin, Editor ou Leitor)
- Listar usuários cadastrados
- Atualizar nome, senha e papel

## 2. Gestão de empresas (empresas.py)

Cadastrar empresa com dados como:
- Nome da empresa
- CNPJ
- Contato empresarial
- E-mail empresarial (com confirmação)
- Responsável e CPF
- Endereço completo (CEP, logradouro, número, bairro, cidade, estado)
- Observações
  
Validações:
- CNPJ não pode se repetir
- Senha mínima de 6 caracteres
- Nome do responsável obrigatório
- Listar empresas cadastradas
- Buscar empresa por nome
- Atualizar dados principais e de endereço
- Exclusão lógica: a empresa é marcada como inativa ("ativo": false)
- As empresas são armazenadas em data/empresas.json, incluindo um array de certificados ESG associados

## 3. Certificados ESG (certificados.py)

Funcionalidades:
- Registrar novo certificado para uma empresa ativa, vinculando:
- Nome do certificado
- Categoria
- Entidade emissora
- Data de emissão
- Data de validade
- Ranking de empresas por número de certificados
- Soma quantos certificados cada empresa ativa possui
- Exibe um ranking ordenado da empresa com mais certificados para a com menos

## 🧱 Regras de negócio (resumo)

- Usuário não pode ser cadastrado com nome duplicado
- CNPJ não pode se repetir entre empresas
- Exclusões são lógicas, usando o campo ativo
- Senhas exigem mínimo de 6 caracteres
- Apenas empresas ativas podem receber novos certificados
- O ranking considera apenas empresas ativas e certificados cadastrados

## 🌐 Site do projeto

Mais detalhes sobre o contexto do projeto podem ser encontrados no site do grupo:
```bash
https://sites.google.com/cesar.school/grupo-8-si/
```

## 👥 Equipe

- Caique Assunção
- Igor Aragão
- Jean Augusto
- Pedro Henrique

