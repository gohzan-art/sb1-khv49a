import discord

async def add_item(ctx, item_name, quantity, db_pool):
    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO inventory (item_name, quantity)
            VALUES ($1, $2)
            ON CONFLICT (item_name) DO UPDATE
            SET quantity = inventory.quantity + $2
        ''', item_name.lower(), quantity)

    await ctx.send(f"Added {quantity} {item_name}(s) to the inventory.")

async def remove_item(ctx, item_name, quantity, db_pool):
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow('''
            UPDATE inventory
            SET quantity = quantity - $2
            WHERE item_name = $1 AND quantity >= $2
            RETURNING quantity
        ''', item_name.lower(), quantity)

    if result:
        await ctx.send(f"Removed {quantity} {item_name}(s) from the inventory. Remaining: {result['quantity']}")
    else:
        await ctx.send(f"Not enough {item_name}(s) in the inventory.")

async def list_inventory(ctx, db_pool):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch('''
            SELECT item_name, quantity
            FROM inventory
            ORDER BY item_name
        ''')

    if not rows:
        await ctx.send("The inventory is empty.")
        return

    embed = discord.Embed(title="Inventory", color=discord.Color.blue())
    for row in rows:
        embed.add_field(name=row['item_name'].capitalize(), value=f"Quantity: {row['quantity']}", inline=True)

    await ctx.send(embed=embed)