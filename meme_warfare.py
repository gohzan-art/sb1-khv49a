import discord
import random

async def handle_meme(ctx, action, args, db_pool):
    if action == "submit":
        await submit_meme(ctx, args, db_pool)
    elif action == "vote":
        await vote_meme(ctx, args, db_pool)
    elif action == "leaderboard":
        await meme_leaderboard(ctx, db_pool)
    else:
        await ctx.send("Invalid action. Use 'submit', 'vote', or 'leaderboard'.")

async def submit_meme(ctx, args, db_pool):
    if len(args) < 1 or not ctx.message.attachments:
        await ctx.send("Usage: !meme submit <title> (with an attached image)")
        return

    title = " ".join(args)
    image_url = ctx.message.attachments[0].url

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO memes (title, image_url, author_id, votes)
            VALUES ($1, $2, $3, 0)
        ''', title, image_url, ctx.author.id)

    await ctx.send(f"Meme '{title}' submitted successfully!")

async def vote_meme(ctx, args, db_pool):
    if len(args) < 1:
        await ctx.send("Usage: !meme vote <meme_id>")
        return

    meme_id = int(args[0])

    async with db_pool.acquire() as conn:
        result = await conn.execute('''
            UPDATE memes
            SET votes = votes + 1
            WHERE id = $1
        ''', meme_id)

    if result == "UPDATE 1":
        await ctx.send(f"Vote recorded for meme {meme_id}")
    else:
        await ctx.send(f"Meme {meme_id} not found")

async def meme_leaderboard(ctx, db_pool):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT id, title, votes, author_id
            FROM memes
            ORDER BY votes DESC
            LIMIT 10
        ''')

    if not rows:
        await ctx.send("No memes found.")
        return

    embed = discord.Embed(title="Meme Warfare Leaderboard", color=discord.Color.gold())
    for i, row in enumerate(rows, 1):
        author = ctx.guild.get_member(row['author_id'])
        author_name = author.display_name if author else "Unknown"
        embed.add_field(
            name=f"{i}. {row['title']} (ID: {row['id']})",
            value=f"Votes: {row['votes']} | Author: {author_name}",
            inline=False
        )

    await ctx.send(embed=embed)