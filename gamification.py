import math
import discord

# Constants for XP and levels
BASE_XP = 100
XP_MULTIPLIER = 1.5

def calculate_level(xp):
    return math.floor(math.log(xp / BASE_XP, XP_MULTIPLIER)) + 1

def calculate_xp_for_level(level):
    return BASE_XP * (XP_MULTIPLIER ** (level - 1))

async def profile(ctx, member, db_pool):
    if member is None:
        member = ctx.author

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow('''
            SELECT fitness_xp, gaming_xp, rank
            FROM members
            WHERE discord_id = $1
        ''', member.id)

    if row:
        total_xp = row['fitness_xp'] + row['gaming_xp']
        level = calculate_level(total_xp)
        next_level_xp = calculate_xp_for_level(level + 1)
        
        embed = discord.Embed(title=f"{member.display_name}'s Profile", color=discord.Color.blue())
        embed.add_field(name="Rank", value=f"{row['rank']}", inline=False)
        embed.add_field(name="Level", value=f"{level}", inline=True)
        embed.add_field(name="Total XP", value=f"{total_xp}/{next_level_xp}", inline=True)
        embed.add_field(name="Fitness XP", value=f"{row['fitness_xp']}", inline=True)
        embed.add_field(name="Gaming XP", value=f"{row['gaming_xp']}", inline=True)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No data found for {member.display_name}")