import discord

async def handle_custom_role(ctx, action, args):
    if action == "create":
        await create_custom_role(ctx, args)
    elif action == "delete":
        await delete_custom_role(ctx, args)
    elif action == "assign":
        await assign_custom_role(ctx, args)
    elif action == "remove":
        await remove_custom_role(ctx, args)
    else:
        await ctx.send("Invalid action. Use 'create', 'delete', 'assign', or 'remove'.")

async def create_custom_role(ctx, args):
    if len(args) < 2:
        await ctx.send("Usage: !custom_role create <role_name> <color_hex>")
        return

    role_name = args[0]
    color_hex = args[1]

    try:
        color = discord.Color(int(color_hex, 16))
    except ValueError:
        await ctx.send("Invalid color hex. Please use a valid hex color code.")
        return

    role = await ctx.guild.create_role(name=role_name, color=color)
    await ctx.send(f"Custom role '{role.name}' created successfully!")

async def delete_custom_role(ctx, args):
    if len(args) < 1:
        await ctx.send("Usage: !custom_role delete <role_name>")
        return

    role_name = " ".join(args)
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await role.delete()
        await ctx.send(f"Custom role '{role_name}' deleted successfully!")
    else:
        await ctx.send(f"Role '{role_name}' not found.")

async def assign_custom_role(ctx, args):
    if len(args) < 2:
        await ctx.send("Usage: !custom_role assign <role_name> <@member>")
        return

    role_name = args[0]
    member = ctx.message.mentions[0] if ctx.message.mentions else None

    if not member:
        await ctx.send("Please mention a member to assign the role.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)
        await ctx.send(f"Role '{role_name}' assigned to {member.display_name}!")
    else:
        await ctx.send(f"Role '{role_name}' not found.")

async def remove_custom_role(ctx, args):
    if len(args) < 2:
        await ctx.send("Usage: !custom_role remove <role_name> <@member>")
        return

    role_name = args[0]
    member = ctx.message.mentions[0] if ctx.message.mentions else None

    if not member:
        await ctx.send("Please mention a member to remove the role from.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        await member.remove_roles(role)
        await ctx.send(f"Role '{role_name}' removed from {member.display_name}!")
    else:
        await ctx.send(f"Role '{role_name}' not found.")