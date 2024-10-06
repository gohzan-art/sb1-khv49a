import discord

async def handle_coc(ctx, action, args, db_pool):
    if action == "set":
        await set_coc(ctx, args, db_pool)
    elif action == "view":
        await view_coc(ctx, db_pool)
    else:
        await ctx.send("Invalid action. Use 'set' or 'view'.")

async def set_coc(ctx, args, db_pool):
    if len(args) < 2:
        await ctx.send("Usage: !coc set <position> <@member>")
        return

    position = args[0]
    member = ctx.message.mentions[0] if ctx.message.mentions else None

    if not member:
        await ctx.send("Please mention a member to set their position.")
        return

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO chain_of_command (position, member_id)
            VALUES ($1, $2)
            ON CONFLICT (position) DO UPDATE
            SET member_id = $2
        ''', position, member.id)

    await ctx.send(f"{member.display_name} has been set as {position} in the chain of command.")

async def view_coc(ctx, db_pool):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT position, member_id
            FROM chain_of_command
            ORDER BY position
        ''')

    if not rows:
        await ctx.send("Chain of command is not set up yet.")
        return

    embed = discord.Embed(title="Chain of Command", color=discord.Color.blue())
    for row in rows:
        member = ctx.guild.get_member(row['member_id'])
        if member:
            embed.add_field(name=row['position'], value=member.mention, inline=False)

    await ctx.send(embed=embed)