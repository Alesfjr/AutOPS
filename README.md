# AutOPS – Automated Operations Monitor
AutOPS é um projeto prático de monitoramento de sistemas, criado para colocar a mão na massa com Python, FastAPI, Docker, Docker Compose e uma arquitetura baseada em agentes.- **Agent**: coleta métricas do sistema operacional


**Agent**: coleta métricas do sistema operacional

**API**: recebe, valida e armazena temporariamente essas métricas

A comunicação entre os serviços ocorre via HTTP dentro de uma rede Docker.

---

## 📌 Arquitetura do Projeto
Agent (psutil)
|
| POST /metrics
v
API (FastAPI)


O Agent roda em loop contínuo, coleta métricas do host/container e envia os dados para a API, que valida o payload usando **Pydantic**.

---

## 📂 Estrutura de Diretórios

autoops-monitor/
│
├── agent/ # Serviço de coleta de métricas
│ ├── init.py
│ ├── collector.py # Loop principal do agent
│ ├── services.py # Regras de avaliação das métricas
│ ├── logs.py # Configuração de logging
│ └── requirements.txt
│
├── api/ # Serviço de API
│ ├── init.py
│ ├── main.py # Aplicação FastAPI
│ └── requirements.txt
│
├── docker/ # Dockerfiles separados por serviço
│ ├── Dockerfile.agent
│ └── Dockerfile.api
│
├── docker-compose.yml # Orquestração dos serviços
└── README.md

---

## 🧠 Funcionamento do Agent

O Agent executa continuamente as seguintes etapas:

1. Coleta métricas do sistema:
   - Uso de CPU (%)
   - Uso de memória (%)
   - Uso de disco (%)
   - Load average (1 minuto)

2. Avalia o estado do sistema localmente (OK / WARN / CRITICAL)

3. Envia as métricas brutas para a API via HTTP (`POST /metrics`)

4. Aguarda um intervalo fixo de 5 segundos antes da próxima coleta

Esse comportamento simula agentes reais de monitoramento utilizados em ambientes de produção.

---

## 🌐 API (FastAPI)

A API fornece:

- Endpoint `/health` para verificação de status
- Endpoint `/metrics` para recebimento de métricas
- Validação automática de payload com **Pydantic**
- Retorno de erro `422 Unprocessable Entity` quando o contrato não é respeitado

A documentação interativa pode ser acessada em:

http://localhost:8000/docs

---

## 🐳 Docker e Docker Compose

Cada serviço possui seu próprio Dockerfile, garantindo isolamento de dependências e builds independentes.

O `docker-compose.yml` é responsável por:

- Subir os containers do Agent e da API
- Criar uma rede interna entre eles
- Permitir que o Agent acesse a API utilizando o hostname `api`

---

## ▶️ Como Executar o Projeto

### Pré-requisitos`

- Docker
- Docker Compose (v2)

### Subir os serviços`

```bash
docker compose up --build
