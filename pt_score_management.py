import discord

async def handle_pt_score(ctx, member, scores, db_pool):
    if not member:
        member = ctx.author

    if not scores:
        await display_pt_score(ctx, member, db_pool)
    else:
        await update_pt_score(ctx, member, scores, db_pool)

async def display_pt_score(ctx, member, db_pool):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow('''
            SELECT pushups, situps, run_time
            FROM pt_scores
            WHERE member_id = $1
            ORDER BY date DESC
            LIMIT 1
        ''', member.id)

    if row:
        embed = discord.Embed(title=f"PT Score for {member.display_name}", color=discord.Color.green())
        embed.add_field(name="Pushups", value=row['pushups'], inline=True)
        embed.add_field(name="Situps", value=row['situps'], inline=True)
        embed.add_field(name="2-Mile Run", value=f"{row['run_time']} minutes", inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No PT score found for {member.display_name}")

async def update_pt_score(ctx, member, scores, db_pool):
    if len(scores) != 3:
        await ctx.send("Usage: !pt_score @member <pushups> <situps> <run_time>")
        return

    pushups, situps, run_time = map(int, scores)

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO pt_scores (member_id, pushups, situps, run_time, date)
            VALUES ($1, $2, $3, $4, CURRENT_DATE)
        ''', member.id, pushups, situps, run_time)

    await ctx.send(f"PT score updated for {member.display_name}")
    await display_pt_score(ctx, member, db_pool)