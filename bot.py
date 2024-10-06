# Add these imports at the top of the file
import asyncio
import youtube_dl
from discord import FFmpegPCMAudio
from discord.utils import get

# Add these variables after the bot initialization
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

# Add this new command in the bot.py file
@bot.command(name='play')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    channel = ctx.message.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()

    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop)
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))

    await ctx.send(f'**Now playing:** {filename}')

# Add this command to stop the music and disconnect the bot
@bot.command(name='stop')
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# Update the on_ready function to include the new commands
@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    await create_db_pool()
    await setup_database()
    logger.info("Bot is fully operational!")
    
    # Add the new commands to the help message
    bot.add_command(play)
    bot.add_command(stop)