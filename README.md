# Movimento Convívio Tabor — Site Institucional

Sistema web para centralizar informações do Movimento Convívio Tabor, servindo tanto à administração (Conselho e Padre) quanto aos membros da comunidade.

## 📋 Sobre o projeto

O site tem como objetivo ser o ponto central de comunicação da pastoral, permitindo:
- Divulgação de eventos e atividades da comunidade
- Consulta de informações institucionais (sobre o movimento, propósito, etc.)
- Gestão de conteúdo por parte do Conselho e do Padre responsável

## 🛠️ Tecnologias utilizadas

- **Backend:** Python 3.14 + Django 6.0.7
- **Banco de dados:** SQLite (ambiente de desenvolvimento)
- **Frontend:** Django Templates (HTML)

## 👥 Perfis de usuário

| Perfil | Permissões atuais |
|---|---|
| **Conselho / Padre** | Administram o sistema via Django Admin (gestão de eventos e usuários) |
| **Membros** | Visualização de eventos e conteúdo institucional |

> **Roadmap:** implementação de níveis de permissão mais granulares dentro do Conselho, definindo até onde cada função administrativa pode alterar o sistema.

## 🚀 Como rodar o projeto localmente

### Pré-requisitos
- Python 3.14+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/movimento-core.git
cd movimento-core

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo .env na raiz do projeto com:
# DJANGO_SECRET_KEY=sua-chave-aqui
# DJANGO_DEBUG=True

# Rode as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Suba o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` para o site e `http://127.0.0.1:8000/admin` para a administração.

## 📁 Estrutura do projeto

## 📌 Status do projeto

Em desenvolvimento ativo — funcionalidades e estrutura ainda em evolução.