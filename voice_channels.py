import discord
from discord.ext import commands

async def create_temp_voice_channel(ctx, channel_name: str):
    category = discord.utils.get(ctx.guild.categories, name="🕹️ Team Operations")
    if not category:
        await ctx.send("The '🕹️ Team Operations' category doesn't exist. Please set up the server first.")
        return

    try:
        channel = await category.create_voice_channel(channel_name)
        await ctx.send(f"Temporary voice channel '{channel_name}' has been created!")

        def check(_, before, after):
            return len(channel.members) == 0 and before.channel == channel

        await bot.wait_for('voice_state_update', check=check)
        await channel.delete()
        await ctx.send(f"Temporary voice channel '{channel_name}' has been deleted due to inactivity.")

    except discord.errors.Forbidden:
        await ctx.send("I don't have permission to create voice channels.")
    except Exception as e:
        await ctx.send(f"An error occurred while creating the voice channel: {str(e)}")