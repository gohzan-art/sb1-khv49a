import discord
from datetime import datetime, timedelta

async def create_event(ctx, name, description, start_time, duration, event_type, db_pool):
    try:
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=duration)

        async with db_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO events (name, description, start_time, end_time, created_by, event_type)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''', name, description, start_datetime, end_datetime, ctx.author.id, event_type)

        embed = discord.Embed(title="New Event Created", color=discord.Color.green())
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Start Time", value=start_datetime.strftime("%Y-%m-%d %H:%M"), inline=True)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Type", value=event_type.capitalize(), inline=True)
        embed.set_footer(text=f"Created by {ctx.author.display_name}")

        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD HH:MM")

async def list_events(ctx, event_type, db_pool):
    query = '''
        SELECT name, description, start_time, end_time, event_type
        FROM events
        WHERE end_time > CURRENT_TIMESTAMP
    '''
    params = []

    if event_type:
        query += " AND event_type = $1"
        params.append(event_type.lower())

    query += " ORDER BY start_time LIMIT 5"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    if not rows:
        await ctx.send("No upcoming events.")
        return

    embed = discord.Embed(title="Upcoming Events", color=discord.Color.blue())
    for row in rows:
        embed.add_field(
            name=f"{row['name']} ({row['event_type'].capitalize()})",
            value=f"**Description:** {row['description']}\n"
                  f"**Start:** {row['start_time'].strftime('%Y-%m-%d %H:%M')}\n"
                  f"**End:** {row['end_time'].strftime('%Y-%m-%d %H:%M')}",
            inline=False
        )

    await ctx.send(embed=embed)