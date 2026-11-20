import asyncio
import time
import asyncpg

DB_DSN = "postgresql://postgres:password@localhost:5433/helpdesk"


async def fetch_email_tickets(fail: bool = False) -> list[dict]:
    await asyncio.sleep(1.0)
    if fail:
        raise ConnectionError("email server timed out")
    return [
        {"customer_id": 1, "issue": "[email] cannot reset account password"},
        {"customer_id": 2, "issue": "[email] duplicate charge on invoice"},
        {"customer_id": 3, "issue": "[email] 2fa code not arriving"},
    ]


async def fetch_chat_tickets(fail: bool = False) -> list[dict]:
    await asyncio.sleep(0.8)
    if fail:
        raise TimeoutError("chat websocket disconnected")
    return [
        {"customer_id": 4, "issue": "[chat] dashboard fails to load"},
        {"customer_id": 5, "issue": "[chat] export button unresponsive"},
        {"customer_id": 6, "issue": "[chat] need help upgrading plan"},
    ]


async def fetch_phone_tickets(fail: bool = False) -> list[dict]:
    await asyncio.sleep(1.2)
    if fail:
        raise RuntimeError("phone webhook returned 503")
    return [
        {"customer_id": 7, "issue": "[phone] complete service outage"},
        {"customer_id": 8, "issue": "[phone] locked out after failed logins"},
    ]


async def run_sequential() -> tuple[list[dict], float]:
    start = time.perf_counter()
    tickets = []
    for fetch_fn in (fetch_email_tickets, fetch_chat_tickets, fetch_phone_tickets):
        tickets.extend(await fetch_fn())
    elapsed = time.perf_counter() - start
    return tickets, elapsed


async def run_concurrent(fail_phone: bool = False) -> tuple[list[dict], list[str], float]:
    start = time.perf_counter()
    channels = [
        ("email", fetch_email_tickets()),
        ("chat", fetch_chat_tickets()),
        ("phone", fetch_phone_tickets(fail=fail_phone)),
    ]

    # return_exceptions=True keeps one broken channel from cancelling the rest
    results = await asyncio.gather(
        *(coro for _, coro in channels),
        return_exceptions=True,
    )

    tickets = []
    errors = []
    for (name, _), result in zip(channels, results):
        if isinstance(result, Exception):
            errors.append(f"{name}: {result}")
        else:
            tickets.extend(result)

    elapsed = time.perf_counter() - start
    return tickets, errors, elapsed


async def save_single_ticket(
    pool: asyncpg.Pool,
    sem: asyncio.Semaphore,
    ticket: dict,
) -> int:
    # cap active db writes at 5 at a time
    async with sem:
        async with pool.acquire() as conn:
            async with conn.transaction():
                ticket_id = await conn.fetchval(
                    """
                    INSERT INTO tickets (customer_id, issue, status)
                    VALUES ($1, $2, 'open')
                    RETURNING id
                    """,
                    ticket["customer_id"],
                    ticket["issue"],
                )
                await conn.execute(
                    """
                    INSERT INTO ticket_events (ticket_id, event_type)
                    VALUES ($1, 'add')
                    """,
                    ticket_id,
                )
                return ticket_id


async def save_tickets_to_db(
    pool: asyncpg.Pool,
    tickets: list[dict],
    max_concurrent: int = 5,
) -> list[int]:
    sem = asyncio.Semaphore(max_concurrent)
    return await asyncio.gather(
        *(save_single_ticket(pool, sem, t) for t in tickets)
    )


async def main() -> None:
    seq_tickets, seq_time = await run_sequential()
    print(f"Sequential: {len(seq_tickets)} tickets in {seq_time:.2f}s")

    conc_tickets, errors, conc_time = await run_concurrent()
    print(f"Concurrent: {len(conc_tickets)} tickets in {conc_time:.2f}s (errors: {len(errors)})")

    # simulate phone failing while email and chat still succeed
    partial_tickets, partial_errors, partial_time = await run_concurrent(fail_phone=True)
    print(
        f"Fault-isolated: {len(partial_tickets)} tickets in {partial_time:.2f}s "
        f"| failed -> {partial_errors}"
    )

    pool = await asyncpg.create_pool(DB_DSN, min_size=1, max_size=5)
    try:
        saved_ids = await save_tickets_to_db(pool, conc_tickets, max_concurrent=5)
        print(f"Saved {len(saved_ids)} tickets to Postgres (IDs: {saved_ids[0]}..{saved_ids[-1]})")
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())