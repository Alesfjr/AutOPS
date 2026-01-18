-- Criação do banco de dados (caso o Docker não crie automaticamente)
CREATE DATABASE IF NOT EXISTS autops;
USE autops;

-- 1. Tabela de Hosts (Identificação)
CREATE TABLE IF NOT EXISTS hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(100) UNIQUE NOT NULL,
    ip VARCHAR(50),
    environment VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Métricas (Armazenamento numérico)
CREATE TABLE IF NOT EXISTS metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    metric_value FLOAT NOT NULL,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE CASCADE
);

-- 3. Tabela de Eventos (Decisões/Alertas)
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    event_type VARCHAR(50),
    severity VARCHAR(20),
    description TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME NULL,
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE CASCADE
);

-- 4. Tabela de Ações (Respostas Automáticas)
CREATE TABLE IF NOT EXISTS actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    action_type VARCHAR(50),
    status VARCHAR(20),
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);