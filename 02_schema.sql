-- Esquemas y tablas de ejemplo (ajusta a tus necesidades)
CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.customers (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS core.accounts (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES core.customers(id),
    number VARCHAR(32) UNIQUE NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    balance NUMERIC(18,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
