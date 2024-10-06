import discord

async def handle_customization(ctx, action, args, db_pool):
    if action == "theme":
        await set_theme(ctx, args, db_pool)
    elif action == "welcome":
        await set_welcome_message(ctx, args, db_pool)
    elif action == "rules":
        await set_rules(ctx, args, db_pool)
    else:
        await ctx.send("Invalid action. Use 'theme', 'welcome', or 'rules'.")

async def set_theme(ctx, args, db_pool):
    if len(args) < 3:
        await ctx.send("Usage: !customize theme <banner_url> <icon_url> <primary_color>")
        return

    banner_url, icon_url, primary_color = args[:3]

    try:
        color = discord.Color(int(primary_color, 16))
    except ValueError:
        await ctx.send("Invalid color hex. Please use a valid hex color code.")
        return

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO server_theme (banner_url, icon_url, primary_color)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO UPDATE
            SET banner_url = $1, icon_url = $2, primary_color = $3
        ''', banner_url, icon_url, primary_color)

    await ctx.guild.edit(banner=banner_url, icon=icon_url)
    await ctx.send("Server theme updated successfully!")

async def set_welcome_message(ctx, args, db_pool):
    if len(args) < 1:
        await ctx.send("Usage: !customize welcome <welcome_message>")
        return

    welcome_message = " ".join(args)

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO server_settings (key, value)
            VALUES ('welcome_message', $1)
            ON CONFLICT (key) DO UPDATE
            SET value = $1
        ''', welcome_message)

    await ctx.send("Welcome message updated successfully!")

async def set_rules(ctx, args, db_pool):
    if len(args) < 1:
        await ctx.send("Usage: !customize rules <rules_text>")
        return

    rules_text = " ".join(args)

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO server_settings (key, value)
            VALUES ('rules', $1)
            ON CONFLICT (key) DO UPDATE
            SET value = $1
        ''', rules_text)

    rules_channel = discord.utils.get(ctx.guild.text_channels, name="rules-and-info")
    if rules_channel:
        await rules_channel.purge()
        await rules_channel.send(rules_text)

    await ctx.send("Server rules updated successfully!")