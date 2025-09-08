-- Datos semilla mínimos (elimina si no deseas seed)
INSERT INTO core.customers (full_name, email)
VALUES ('Cliente Demo', 'demo@example.com')
ON CONFLICT (email) DO NOTHING;

INSERT INTO core.accounts (customer_id, number, currency, balance)
SELECT id, '000123456789', 'USD', 100.00
FROM core.customers
WHERE email = 'demo@example.com'
ON CONFLICT DO NOTHING;
