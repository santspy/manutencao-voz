# 🎙️ Manutenção por Voz (Voice-to-OS)

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Sobre o Projeto
Este projeto resolve uma dor real da indústria: técnicos de manutenção de campo perdem muito tempo preenchendo relatórios em papel ou sistemas lentos no final do turno, resultando em dados imprecisos e perda de histórico.

A solução é um PWA (Progressive Web App) de inspeção por voz. O técnico segura o botão, dita o problema (ex: "Rolamento do motor 3 com vibração"), e o sistema transcreve o áudio, classifica a categoria do problema (Mecânica, Elétrica, Geral) e gera uma Ordem de Serviço (OS) automaticamente no banco de dados.

## 🖼️ Demonstração

### Interface de Inspeção por Voz
![Frontend do Sistema](images/frontend.png)

### Documentação da API (Swagger)
![Swagger UI](images/swagger.png)

### Pipeline de CI/CD (GitHub Actions)
![GitHub Actions](images/actions.png)

## 🚀 Tecnologias Utilizadas
* **Frontend:** HTML5, CSS3, JavaScript (Web Speech API para transcrição em tempo real).
* **Backend:** Python 3.12, FastAPI, SQLModel (ORM).
* **Banco de Dados:** PostgreSQL 16.
* **Infraestrutura:** Docker e Docker Compose (Multi-stage builds, Healthchecks).
* **Observabilidade:** Logs estruturados em JSON (Structlog) com `Correlation ID`.
* **CI/CD:** GitHub Actions (Pytest + Gitleaks para segurança).

## 🏗️ Arquitetura da Solução

```text
[ Celular/Navegador ] 
       │ (Áudio -> Texto)
       ▼
[ Frontend Nginx ] ──(HTTP POST)──> [ Backend FastAPI ] ──(SQL)──> [ PostgreSQL ]
  (Porta 3000)                        (Porta 8000)
Frontend: Servido via Nginx em um container Alpine super leve.

Backend: API REST que processa a regra de negócio e classifica o texto.

Segurança: Middleware de CORS configurado e pipeline de CI que escaneia segredos vazados.

Logs: Todas as requisições geram um log em JSON com um correlation_id único para facilitar o rastreio em ferramentas como Datadog/Grafana.

### Como rodar o projeto localmente
Pré-requisitos
Docker e Docker Compose instalados.

Navegador baseado em Chromium (Google Chrome ou Microsoft Edge) para suporte à Web Speech API.

Passo a passo
Clone o repositório:

bash
git clone https://github.com/santspy/manutencao-voz.git
cd manutencao-voz
Suba os containers:

bash
docker compose up --build -d
Acesse a aplicação:

Frontend: http://localhost:3000

Documentação da API (Swagger): http://localhost:8000/docs

## Testes Automatizados
O projeto conta com testes unitários para validar a regra de negócio de classificação das Ordens de Serviço.
Para rodar os testes localmente:

bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
(Os testes também rodam automaticamente no GitHub Actions a cada Pull Request ou Push na branch main).

## Segurança e Boas Práticas
Gitleaks: O pipeline de CI impede que senhas ou tokens acidentais sejam comitados.

Healthchecks: O banco de dados PostgreSQL possui um healthcheck; a API só inicia depois que o banco está 100% pronto para receber conexões.

CORS: Configurado estritamente para permitir a comunicação entre o Frontend e o Backend.

Logs Sanitizados: O sistema não salva áudio bruto nem dados sensíveis nos logs, apenas metadados da requisição.

## Autor
Orlando Santana (santspy)

LinkedIn: Orlando Santana

GitHub: @santspy

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Demonstração

### Interface de Inspeção por Voz
![Frontend do Sistema](images/frontend.png)

### Documentação da API (Swagger)
![Swagger UI](images/swagger.png)

### Pipeline de CI/CD (GitHub Actions)
![GitHub Actions](images/actions.png)