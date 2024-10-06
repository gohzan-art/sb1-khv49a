import discord
from datetime import datetime
from collections import defaultdict

async def mark_attendance(ctx, member, status, db_pool):
    valid_statuses = ['present', 'leave', 'quarters', 'comp', 'awol', 'school', 'tdy']
    if status.lower() not in valid_statuses:
        await ctx.send(f"Invalid status. Please use one of: {', '.join(valid_statuses)}")
        return

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO attendance_logs (member_id, date, status)
            VALUES ($1, $2, $3)
            ON CONFLICT (member_id, date) DO UPDATE
            SET status = $3
        ''', member.id, datetime.now().date(), status.lower())

    await ctx.send(f"Attendance for {member.display_name} marked as {status}.")

async def generate_report(ctx, start_date, end_date, db_pool):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD.")
        return

    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT member_id, status, COUNT(*) as count
            FROM attendance_logs
            WHERE date BETWEEN $1 AND $2
            GROUP BY member_id, status
            ORDER BY member_id, status
        ''', start, end)

    report = defaultdict(lambda: defaultdict(int))
    for row in rows:
        report[row['member_id']][row['status']] = row['count']

    embed = discord.Embed(title="Attendance Report", color=discord.Color.blue())
    for member_id, statuses in report.items():
        member = ctx.guild.get_member(member_id)
        if member:
            status_str = ", ".join(f"{status}: {count}" for status, count in statuses.items())
            embed.add_field(name=member.display_name, value=status_str, inline=False)

    await ctx.send(embed=embed)