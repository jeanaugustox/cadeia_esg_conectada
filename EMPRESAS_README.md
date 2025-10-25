# 🏢 Módulo de Gestão de Empresas

Este módulo implementa um CRUD completo para gerenciamento de empresas no sistema Cadeia ESG Conectada.

## 📋 Funcionalidades

### ✅ Operações CRUD
- **CREATE**: Cadastrar nova empresa
- **READ**: Listar e buscar empresas
- **UPDATE**: Atualizar dados de empresa existente
- **DELETE**: Excluir empresa (marca como inativa)

### 🔍 Validações Implementadas
- Validação de CNPJ (formato básico)
- Validação de CPF (formato básico)
- Validação de email
- Verificação de CNPJ duplicado
- Confirmação de email
- Validação de senha (mínimo 6 caracteres)

## 🚀 Como Usar

### Executar o Sistema Completo
```bash
cd cadeia_esg_conectada
python src/app.py
```

### Executar Apenas o Módulo de Empresas
```bash
cd cadeia_esg_conectada
python src/empresas.py
```

### Executar Exemplo Programático
```bash
cd cadeia_esg_conectada
python exemplo_uso.py
```

## 📊 Estrutura de Dados

Cada empresa é armazenada com a seguinte estrutura:

```json
{
  "id": 1,
  "nome_empresa": "Nome da Empresa",
  "cnpj": "12.345.678/0001-90",
  "contato_empresarial": "(11) 99999-9999",
  "email_empresarial": "contato@empresa.com.br",
  "nome_responsavel": "Nome do Responsável",
  "cpf_responsavel": "123.456.789-00",
  "outro_contato": "(11) 88888-8888",
  "nome_usuario": "usuario",
  "senha": "senha123",
  "endereco": {
    "cep": "01234-567",
    "logradouro": "Rua das Flores, 123",
    "numero": "123",
    "complemento": "Sala 45",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP"
  },
  "observacoes": "Observações adicionais",
  "data_cadastro": "15/12/2024 10:30:00",
  "ativo": true
}
```

## 🔧 Funções Principais

### `cadastrar_empresa()`
Cadastra uma nova empresa com validações completas.

### `listar_empresas()`
Lista todas as empresas cadastradas com informações resumidas.

### `buscar_empresa_por_cnpj()`
Busca uma empresa específica pelo CNPJ e exibe todos os dados.

### `atualizar_empresa()`
Permite editar dados de uma empresa existente.

### `excluir_empresa()`
Marca uma empresa como inativa (soft delete).

### `menu_empresas()`
Menu interativo para gerenciar empresas.

## 📁 Arquivos

- `src/empresas.py` - Módulo principal com todas as funções
- `data/empresas.json` - Arquivo de dados (criado automaticamente)
- `exemplo_uso.py` - Exemplo de uso programático
- `src/app.py` - Sistema principal integrado

## 🎯 Características do Código

- **Simples**: Código procedural fácil de entender
- **Organizado**: Funções bem estruturadas e documentadas
- **Robusto**: Validações e tratamento de erros
- **Flexível**: Fácil de estender e modificar
- **Educativo**: Ideal para aprendizado de programação

## 🔒 Segurança

⚠️ **Nota Importante**: Este é um sistema educacional. Em produção, implemente:
- Hash de senhas (bcrypt, scrypt, etc.)
- Validações mais robustas de CNPJ/CPF
- Criptografia de dados sensíveis
- Controle de acesso por usuário

## 📝 Exemplo de Uso Programático

```python
from src.empresas import *

# Carregar empresas
empresas = carregar_empresas()

# Cadastrar nova empresa
nova_empresa = {
    "id": len(empresas) + 1,
    "nome_empresa": "Minha Empresa",
    "cnpj": "12.345.678/0001-90",
    # ... outros campos
}

empresas.append(nova_empresa)
salvar_empresas(empresas)
```

## 🎓 Aprendizado

Este módulo demonstra conceitos importantes:
- Manipulação de arquivos JSON
- Validação de dados
- Estruturas de dados em Python
- Programação procedural
- Tratamento de erros
- Interface de linha de comando
