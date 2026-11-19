-- teams and tags
INSERT INTO teams (name) VALUES
    ('Tech'),
    ('Billing'),
    ('Support'),
    ('Security'),
    ('Onboarding');

INSERT INTO tags (name) VALUES
    ('login'),
    ('urgent'),
    ('billing'),
    ('refund'),
    ('bug'),
    ('outage'),
    ('account'),
    ('feature');

-- agents and customers
INSERT INTO agents (name, team_id)
SELECT
    'Agent ' || g,
    ((g - 1) % 5) + 1
FROM generate_series(1, 25) AS g;

INSERT INTO customers (name, email, phone)
SELECT
    'Customer ' || g,
    'customer' || g || '@example.com',
    '0300' || LPAD(g::text, 7, '0')
FROM generate_series(1, 2500) AS g;

-- 50k tickets (leaving last 100 customers and 5 agents light for the queries)
WITH series AS (
    SELECT
        g,
        random() AS r,
        NOW() - (random() * interval '90 days') AS created_at
    FROM generate_series(1, 50000) AS g
),
raw_tickets AS (
    SELECT
        (1 + floor(random() * 2400))::int AS customer_id,
        CASE
            WHEN g % 250 = 0 THEN (21 + floor(random() * 5))::int
            ELSE (1 + floor(random() * 20))::int
        END AS agent_id,
        'Issue #' || g || ': ' || (ARRAY[
            'Login fails',
            'Refund requested',
            'Payment declined',
            'App crashes on startup',
            'Cannot reset password',
            'Invoice discrepancy',
            'Slow dashboard performance'
        ])[1 + floor(random() * 7)::int] AS issue,
        CASE
            WHEN r < 0.05 THEN 'open'
            WHEN r < 0.20 THEN 'in_progress'
            ELSE 'resolved'
        END AS status,
        created_at
    FROM series
)
INSERT INTO tickets (customer_id, agent_id, issue, status, created_at, resolved_at)
SELECT
    customer_id,
    agent_id,
    issue,
    status,
    created_at,
    CASE
        WHEN status = 'resolved'
        THEN created_at + (interval '30 minutes' + random() * interval '72 hours')
        ELSE NULL
    END AS resolved_at
FROM raw_tickets;

-- 1 or 2 tags per ticket
INSERT INTO ticket_tags (ticket_id, tag_id)
SELECT id, (1 + floor(random() * 8))::int
FROM tickets;

INSERT INTO ticket_tags (ticket_id, tag_id)
SELECT id, (1 + floor(random() * 8))::int
FROM tickets
WHERE random() < 0.5
ON CONFLICT DO NOTHING;

-- ticket events
INSERT INTO ticket_events (ticket_id, agent_id, event_type, created_at)
SELECT id, agent_id, 'add', created_at
FROM tickets;

INSERT INTO ticket_events (ticket_id, agent_id, event_type, created_at)
SELECT id, agent_id, 'resolve', resolved_at
FROM tickets
WHERE status = 'resolved';

ANALYZE;