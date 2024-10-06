import discord
from datetime import datetime

async def handle_training(ctx, action, args, db_pool):
    if action == "schedule":
        await schedule_training(ctx, args, db_pool)
    elif action == "complete":
        await complete_training(ctx, args, db_pool)
    elif action == "list":
        await list_trainings(ctx, db_pool)
    else:
        await ctx.send("Invalid action. Use 'schedule', 'complete', or 'list'.")

async def schedule_training(ctx, args, db_pool):
    if len(args) < 3:
        await ctx.send("Usage: !training schedule <name> <date> <description>")
        return
    
    name, date, description = args[0], args[1], " ".join(args[2:])
    
    try:
        training_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await ctx.send("Invalid date format. Use YYYY-MM-DD.")
        return

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO trainings (name, date, description, created_by)
            VALUES ($1, $2, $3, $4)
        ''', name, training_date, description, ctx.author.id)

    await ctx.send(f"Training '{name}' scheduled for {date}.")

async def complete_training(ctx, args, db_pool):
    if len(args) < 1:
        await ctx.send("Usage: !training complete <training_id>")
        return
    
    training_id = args[0]
    
    async with db_pool.acquire() as conn:
        result = await conn.execute('''
            UPDATE trainings
            SET completed = TRUE
            WHERE id = $1
        ''', int(training_id))

    if result == "UPDATE 1":
        await ctx.send(f"Training {training_id} marked as completed.")
    else:
        await ctx.send(f"Training {training_id} not found.")

async def list_trainings(ctx, db_pool):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT id, name, date, description, completed
            FROM trainings
            ORDER BY date
        ''')

    if not rows:
        await ctx.send("No trainings scheduled.")
        return

    embed = discord.Embed(title="Scheduled Trainings", color=discord.Color.blue())
    for row in rows:
        status = "Completed" if row['completed'] else "Scheduled"
        embed.add_field(
            name=f"{row['id']}. {row['name']} ({status})",
            value=f"Date: {row['date'].strftime('%Y-%m-%d')}\nDescription: {row['description']}",
            inline=False
        )

    await ctx.send(embed=embed)