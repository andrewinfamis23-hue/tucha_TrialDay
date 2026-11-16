-- Только синтетический WMS-мок. Скрипт выполняется в отдельном Docker volume.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'crm_sandbox') THEN
        CREATE ROLE crm_sandbox LOGIN PASSWORD 'crm-sandbox-local-only' NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

GRANT CONNECT, TEMPORARY ON DATABASE tucha_sandbox TO crm_sandbox;
GRANT USAGE, CREATE ON SCHEMA public TO crm_sandbox;

CREATE SCHEMA IF NOT EXISTS wms_mock;

CREATE TABLE IF NOT EXISTS wms_mock.operation (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_id text NOT NULL UNIQUE,
    operation_type text NOT NULL CHECK (operation_type IN ('inbound', 'outbound')),
    document_state text NOT NULL,
    planned_at timestamptz NOT NULL,
    customer_code text NOT NULL
);

CREATE TABLE IF NOT EXISTS wms_mock.operation_line (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    operation_id bigint NOT NULL REFERENCES wms_mock.operation(id),
    product_ref text NOT NULL,
    quantity numeric(16, 3),
    uom text NOT NULL
);

INSERT INTO wms_mock.operation
    (external_id, operation_type, document_state, planned_at, customer_code)
SELECT
    'MOCK-' || to_char(number, 'FM000'),
    CASE WHEN number % 2 = 0 THEN 'inbound' ELSE 'outbound' END,
    CASE WHEN number % 3 = 0 THEN 'completed' ELSE 'planned' END,
    timestamptz '2026-11-16 08:00:00+03' + number * interval '2 hours',
    'FAKE-' || ((number - 1) % 5 + 1)
FROM generate_series(1, 20) AS number
ON CONFLICT (external_id) DO NOTHING;

INSERT INTO wms_mock.operation_line (operation_id, product_ref, quantity, uom)
SELECT operation.id, 'SKU-' || to_char(line_no, 'FM000'), operation.id + line_no, 'шт'
FROM wms_mock.operation AS operation
CROSS JOIN generate_series(1, 3) AS line_no
WHERE NOT EXISTS (
    SELECT 1 FROM wms_mock.operation_line AS existing
    WHERE existing.operation_id = operation.id AND existing.product_ref = 'SKU-' || to_char(line_no, 'FM000')
);

REVOKE CREATE ON SCHEMA wms_mock FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA wms_mock FROM PUBLIC;
GRANT USAGE ON SCHEMA wms_mock TO crm_sandbox;
GRANT SELECT ON ALL TABLES IN SCHEMA wms_mock TO crm_sandbox;
