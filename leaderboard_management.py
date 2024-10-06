import discord

async def show_leaderboard(ctx, board_type, db_pool):
    if board_type.lower() not in ["overall", "fitness", "gaming"]:
        await ctx.send("Invalid leaderboard type. Please use 'overall', 'fitness', or 'gaming'.")
        return

    async with db_pool.acquire() as conn:
        if board_type.lower() == "overall":
            rows = await conn.fetch('''
                SELECT discord_id, fitness_xp + gaming_xp as total_xp
                FROM members
                ORDER BY total_xp DESC
                LIMIT 10
            ''')
        else:
            xp_column = f"{board_type.lower()}_xp"
            rows = await conn.fetch(f'''
                SELECT discord_id, {xp_column}
                FROM members
                ORDER BY {xp_column} DESC
                LIMIT 10
            ''')

    embed = discord.Embed(title=f"{board_type.capitalize()} Leaderboard", color=discord.Color.gold())
    for i, row in enumerate(rows, 1):
        member = ctx.guild.get_member(row['discord_id'])
        if member:
            xp = row['total_xp'] if board_type.lower() == "overall" else row[f"{board_type.lower()}_xp"]
            embed.add_field(name=f"{i}. {member.display_name}", value=f"XP: {xp}", inline=False)

    await ctx.send(embed=embed)