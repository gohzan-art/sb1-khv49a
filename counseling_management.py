import discord
import asyncio

async def start_counseling(ctx, member, db_pool):
    counseling_channel = await ctx.guild.create_text_channel(f"counseling-{member.name}")
    await counseling_channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await counseling_channel.set_permissions(member, read_messages=True, send_messages=True)
    await counseling_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    await counseling_channel.send(f"{ctx.author.mention} has started a counseling session with {member.mention}. Please begin your discussion.")

    def check(m):
        return m.channel == counseling_channel and m.author != ctx.bot.user

    transcript = []
    while True:
        try:
            message = await ctx.bot.wait_for('message', check=check, timeout=600)
            transcript.append(f"{message.author.display_name}: {message.content}")
            if message.content.lower() == "!endcounseling":
                break
        except asyncio.TimeoutError:
            await counseling_channel.send("Counseling session timed out due to inactivity.")
            break

    async with db_pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO counseling_logs (member_id, counselor_id, transcript)
            VALUES ($1, $2, $3)
        ''', member.id, ctx.author.id, "\n".join(transcript))

    await counseling_channel.delete()
    await ctx.send(f"Counseling session with {member.display_name} has ended and been logged.")