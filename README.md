Projeto da disciplina Projetos 1 — Curso de Sistemas de Informação — CESAR School (Recife-PE)
A "Cadeia ESG Conectada" é um sistema para conectar empresas e fornecedores alinhados a práticas ESG, com objetivo de criar conexões entre marcas com práticas sustentáveis.
Equipe: Caique Assunção, Igor Aragão, Jean Augusto, Pedro Henrique
Estrutura do repositório:
├─ Src/
│  ├─ app.py           # loop principal / menu
│  ├─ auth.py          # autenticação (login/recuperar senha)
│  ├─ certificado/     # módulo(s) de certificados ESG
│  ├─ empresas.py      # CRUD de empresas/fornecedores
│  └─ usuarios.py      # CRUD de usuários
└─ Data/
   ├─ empresas.json    # base local de empresas/fornecedores
   └─ usuarios.json    # base local de usuários
