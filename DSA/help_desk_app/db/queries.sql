-- resolve a ticket atomically
BEGIN;

UPDATE tickets
SET status = 'resolved',
    resolved_at = NOW()
WHERE id = 1
  AND status <> 'resolved';

INSERT INTO ticket_events (ticket_id, agent_id, event_type, created_at)
SELECT id, agent_id, 'resolve', resolved_at
FROM tickets
WHERE id = 1;

COMMIT;