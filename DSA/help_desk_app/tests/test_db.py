import pytest
import asyncpg

from async_intake import (
    DB_DSN,
    run_sequential,
    run_concurrent,
    save_tickets_to_db,
)


@pytest.fixture
async def db_pool():
    pool = await asyncpg.create_pool(DB_DSN, min_size=1, max_size=5)
    yield pool
    await pool.close()


@pytest.mark.asyncio
async def test_schema_and_seed_counts(db_pool):
    async with db_pool.acquire() as conn:
        ticket_count = await conn.fetchval("SELECT COUNT(*) FROM tickets")
        team_count = await conn.fetchval("SELECT COUNT(*) FROM teams")
        agent_count = await conn.fetchval("SELECT COUNT(*) FROM agents")
        customer_count = await conn.fetchval("SELECT COUNT(*) FROM customers")

    assert ticket_count >= 50000
    assert team_count == 5
    assert agent_count == 25
    assert customer_count == 2500


@pytest.mark.asyncio
async def test_analytical_queries(db_pool):
    async with db_pool.acquire() as conn:
        # agents with > 100 resolved tickets (should filter out the 5 low-volume agents)
        high_vol_agents = await conn.fetch(
            """
            SELECT a.id
            FROM agents a
            JOIN tickets t ON a.id = t.agent_id
            WHERE t.status = 'resolved'
            GROUP BY a.id
            HAVING COUNT(t.id) > 100
            """
        )
        assert len(high_vol_agents) == 20

        # customers with zero resolved tickets (last 100 customers were left unseeded)
        unresolved_customers = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM customers c
            WHERE NOT EXISTS (
                SELECT 1
                FROM tickets t
                WHERE t.customer_id = c.id
                  AND t.status = 'resolved'
            )
            """
        )
        assert unresolved_customers >= 100

        # avg resolution time per team returns all 5 teams
        team_avgs = await conn.fetch(
            """
            SELECT tm.name, AVG(t.resolved_at - t.created_at) AS avg_time
            FROM teams tm
            JOIN agents a ON tm.id = a.team_id
            JOIN tickets t ON a.id = t.agent_id
            WHERE t.status = 'resolved' AND t.resolved_at IS NOT NULL
            GROUP BY tm.id, tm.name
            """
        )
        assert len(team_avgs) == 5


@pytest.mark.asyncio
async def test_resolve_ticket_transaction_commits_and_rolls_back(db_pool):
    async with db_pool.acquire() as conn:
        # create a temporary open ticket
        ticket_id = await conn.fetchval(
            """
            INSERT INTO tickets (customer_id, agent_id, issue, status)
            VALUES (1, 1, '[test] transaction check', 'open')
            RETURNING id
            """
        )

        try:
            # simulate a failed transaction and verify rollback keeps status open
            with pytest.raises(RuntimeError):
                async with conn.transaction():
                    await conn.execute(
                        "UPDATE tickets SET status = 'resolved', resolved_at = NOW() WHERE id = $1",
                        ticket_id,
                    )
                    raise RuntimeError("forced failure mid-transaction")

            status_after_rollback = await conn.fetchval(
                "SELECT status FROM tickets WHERE id = $1", ticket_id
            )
            assert status_after_rollback == "open"

            # run the full atomic resolution
            async with conn.transaction():
                await conn.execute(
                    """
                    UPDATE tickets
                    SET status = 'resolved', resolved_at = NOW()
                    WHERE id = $1 AND status <> 'resolved'
                    """,
                    ticket_id,
                )
                await conn.execute(
                    """
                    INSERT INTO ticket_events (ticket_id, agent_id, event_type, created_at)
                    SELECT id, agent_id, 'resolve', resolved_at
                    FROM tickets
                    WHERE id = $1
                    """,
                    ticket_id,
                )

            status_after_commit = await conn.fetchval(
                "SELECT status FROM tickets WHERE id = $1", ticket_id
            )
            event_count = await conn.fetchval(
                "SELECT COUNT(*) FROM ticket_events WHERE ticket_id = $1 AND event_type = 'resolve'",
                ticket_id,
            )
            assert status_after_commit == "resolved"
            assert event_count == 1
        finally:
            await conn.execute("DELETE FROM ticket_events WHERE ticket_id = $1", ticket_id)
            await conn.execute("DELETE FROM tickets WHERE id = $1", ticket_id)


@pytest.mark.asyncio
async def test_async_intake_concurrency_and_fault_isolation():
    seq_tickets, seq_time = await run_sequential()
    conc_tickets, errors, conc_time = await run_concurrent()

    assert len(seq_tickets) == 8
    assert len(conc_tickets) == 8
    assert errors == []
    assert conc_time < seq_time

    # phone fails, email + chat still return their 6 tickets
    partial_tickets, partial_errors, _ = await run_concurrent(fail_phone=True)
    assert len(partial_tickets) == 6
    assert len(partial_errors) == 1
    assert "phone" in partial_errors[0]


@pytest.mark.asyncio
async def test_save_tickets_to_db(db_pool):
    sample = [
        {"customer_id": 1, "issue": "[test] async save 1"},
        {"customer_id": 2, "issue": "[test] async save 2"},
    ]
    saved_ids = await save_tickets_to_db(db_pool, sample, max_concurrent=5)

    try:
        assert len(saved_ids) == 2
        async with db_pool.acquire() as conn:
            event_count = await conn.fetchval(
                "SELECT COUNT(*) FROM ticket_events WHERE ticket_id = ANY($1::int[]) AND event_type = 'add'",
                saved_ids,
            )
            assert event_count == 2
    finally:
        async with db_pool.acquire() as conn:
            await conn.execute("DELETE FROM ticket_events WHERE ticket_id = ANY($1::int[])", saved_ids)
            await conn.execute("DELETE FROM tickets WHERE id = ANY($1::int[])", saved_ids)