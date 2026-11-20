import asyncio
import asyncpg

from async_intake import DB_DSN, run_concurrent, save_tickets_to_db


def read_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid number.")
        return None


async def list_open_tickets(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT t.id, c.name AS customer, COALESCE(a.name, 'Unassigned') AS agent, t.issue
            FROM tickets t
            JOIN customers c ON c.id = t.customer_id
            LEFT JOIN agents a ON a.id = t.agent_id
            WHERE t.status = 'open'
            ORDER BY t.id DESC
            LIMIT 10
            """
        )

    if not rows:
        print("\nNo open tickets.")
        return

    print(f"\nLatest {len(rows)} open tickets:")
    for r in rows:
        print(f"  #{r['id']} | {r['customer']} | Agent: {r['agent']} | {r['issue']}")


async def create_ticket(pool: asyncpg.Pool) -> None:
    customer_id = read_int("Customer ID (1-2500): ")
    if customer_id is None:
        return

    issue = input("Issue description: ").strip()
    if not issue:
        print("Issue cannot be empty.")
        return

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                ticket_id = await conn.fetchval(
                    """
                    INSERT INTO tickets (customer_id, issue, status)
                    VALUES ($1, $2, 'open')
                    RETURNING id
                    """,
                    customer_id,
                    issue,
                )
                await conn.execute(
                    """
                    INSERT INTO ticket_events (ticket_id, event_type)
                    VALUES ($1, 'add')
                    """,
                    ticket_id,
                )
        print(f"Created ticket #{ticket_id} (audit event logged).")
    except asyncpg.ForeignKeyViolationError:
        print(f"Customer ID {customer_id} does not exist.")


async def serve_ticket(pool: asyncpg.Pool) -> None:
    ticket_id = read_int("Ticket ID to serve: ")
    agent_id = read_int("Agent ID (1-25): ")
    if ticket_id is None or agent_id is None:
        return

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                updated = await conn.fetchval(
                    """
                    UPDATE tickets
                    SET status = 'in_progress', agent_id = $2
                    WHERE id = $1 AND status = 'open'
                    RETURNING id
                    """,
                    ticket_id,
                    agent_id,
                )
                if not updated:
                    print(f"Ticket #{ticket_id} not found or not in 'open' status.")
                    return

                await conn.execute(
                    """
                    INSERT INTO ticket_events (ticket_id, agent_id, event_type)
                    VALUES ($1, $2, 'serve')
                    """,
                    ticket_id,
                    agent_id,
                )
        print(f"Ticket #{ticket_id} is now in_progress with agent #{agent_id}.")
    except asyncpg.ForeignKeyViolationError:
        print(f"Agent ID {agent_id} does not exist.")


async def resolve_ticket(pool: asyncpg.Pool) -> None:
    ticket_id = read_int("Ticket ID to resolve: ")
    if ticket_id is None:
        return

    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                UPDATE tickets
                SET status = 'resolved', resolved_at = NOW()
                WHERE id = $1 AND status <> 'resolved'
                RETURNING id, agent_id, resolved_at
                """,
                ticket_id,
            )
            if not row:
                print(f"Ticket #{ticket_id} not found or already resolved.")
                return

            await conn.execute(
                """
                INSERT INTO ticket_events (ticket_id, agent_id, event_type, created_at)
                VALUES ($1, $2, 'resolve', $3)
                """,
                row["id"],
                row["agent_id"],
                row["resolved_at"],
            )
    print(f"Resolved ticket #{ticket_id} (atomic transaction committed).")


async def view_ticket_events(pool: asyncpg.Pool) -> None:
    ticket_id = read_int("Ticket ID: ")
    if ticket_id is None:
        return

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT e.event_type, COALESCE(a.name, 'System') AS agent, e.created_at
            FROM ticket_events e
            LEFT JOIN agents a ON a.id = e.agent_id
            WHERE e.ticket_id = $1
            ORDER BY e.created_at ASC
            """,
            ticket_id,
        )

    if not rows:
        print(f"No events found for ticket #{ticket_id}.")
        return

    print(f"\nAudit trail for ticket #{ticket_id}:")
    for r in rows:
        ts = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [{ts}] {r['event_type']} (by {r['agent']})")


async def trigger_async_intake(pool: asyncpg.Pool) -> None:
    fail_choice = input("Simulate phone channel failure? (y/n): ").strip().lower()
    fail_phone = fail_choice == "y"

    print("Fetching tickets concurrently from email, chat, and phone...")
    tickets, errors, elapsed = await run_concurrent(fail_phone=fail_phone)
    saved_ids = await save_tickets_to_db(pool, tickets, max_concurrent=5)

    print(f"Fetched & saved {len(saved_ids)} tickets in {elapsed:.2f}s (IDs: {saved_ids[0]}..{saved_ids[-1]})")
    if errors:
        print(f"Channel errors isolated -> {errors}")


async def show_team_stats(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                tm.name AS team,
                COUNT(t.id) AS resolved_count,
                AVG(t.resolved_at - t.created_at) AS avg_time
            FROM teams tm
            JOIN agents a ON tm.id = a.team_id
            JOIN tickets t ON a.id = t.agent_id
            WHERE t.status = 'resolved' AND t.resolved_at IS NOT NULL
            GROUP BY tm.id, tm.name
            ORDER BY avg_time ASC
            """
        )

    print("\nTeam Performance:")
    for r in rows:
        avg_hours = r["avg_time"].total_seconds() / 3600
        print(f"  {r['team']:<20} | Resolved: {r['resolved_count']:<6} | Avg time: {avg_hours:.1f} hrs")


async def main() -> None:
    pool = await asyncpg.create_pool(DB_DSN, min_size=1, max_size=5)
    try:
        while True:
            print("\n=== Help Desk (PostgreSQL) ===")
            print("1. List latest open tickets")
            print("2. Create ticket")
            print("3. Assign / serve ticket")
            print("4. Resolve ticket")
            print("5. View ticket audit log")
            print("6. Run async multi-channel intake")
            print("7. Team resolution stats")
            print("0. Exit")

            choice = input("Select option: ").strip()

            if choice == "1":
                await list_open_tickets(pool)
            elif choice == "2":
                await create_ticket(pool)
            elif choice == "3":
                await serve_ticket(pool)
            elif choice == "4":
                await resolve_ticket(pool)
            elif choice == "5":
                await view_ticket_events(pool)
            elif choice == "6":
                await trigger_async_intake(pool)
            elif choice == "7":
                await show_team_stats(pool)
            elif choice == "0":
                break
            else:
                print("Invalid option.")
    finally:
        await pool.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting.")