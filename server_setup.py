import discord
from discord.ext import commands

async def setup_server_layout(ctx, bot):
    guild = ctx.guild
    
    # Delete all existing channels and categories
    for channel in guild.channels:
        await channel.delete()
    
    # Create categories and channels
    categories = {
        "📢 Welcome & Onboarding": [
            "welcome", "rules-and-info", "roles-and-titles", "faq", "readme"
        ],
        "🶂️ Work Stuff (Operations)": [
            "announcements", "training-schedule", "pt-schedule", "pt-scores", "missions-and-tasks", "appointments", "ai-chat"
        ],
        "🏰 Soldier Resources": [
            "blank-forms", "tms", "ltt-conops", "archive-examples", "command-orders"
        ],
        "🕹️ Team Operations": [
            "hangout", "tanker-team", "alpha-team-chat", "bravo-team-chat", "support-team-chat"
        ],
        "💬 General Engagement (Social)": [
            "general", "meme-warfare", "gaming-squad", "youtube", "ai", "meme-generator-and-ranking", "fun-challenges"
        ],
        "📈 Leaderboards & Logs": [
            "fitness-leaderboard", "acft-leaderboard", "gaming-leaderboard", "weapons-qualification-leaderboard", "music-leaderboard", "meme-leaderboard"
        ],
        "📚 Resources and Links": [
            "weekend-adventure-suggestions", "guides-and-documents", "army-links", "external-resources"
        ],
        "📝 Task Creation and Updates": [
            "task-management"
        ],
        "🩺 Medical & Appointments": [
            "medpros-tracker", "medical-appointments", "health-updates"
        ],
        "🔒 Sensitive Items & Property Accountability": [
            "sensitive-items-tracking", "property-accountability", "equipment-roster", "detailed-equipment-overview",
            "vehicles-tracking", "trailers-tracking", "generators-tracking", "connexes-tracking",
            "vehicle-5988-tracking", "additional-inventory", "automated-pmcs-reminders"
        ],
        "🗂️ Soldier Database (NCO/Admin Only)": [
            "counseling-logs", "absence-logs", "soldier-info-database"
        ],
        "📝 Daily/Weekly Reports & Notes": [
            "notes", "notes-archive"
        ]
    }
    
    for category_name, channels in categories.items():
        category = await guild.create_category(category_name)
        for channel_name in channels:
            await category.create_text_channel(channel_name)
    
    # Create voice channels
    team_ops_category = discord.utils.get(guild.categories, name="🕹️ Team Operations")
    await team_ops_category.create_voice_channel("Alpha Team Voice Channel")
    await team_ops_category.create_voice_channel("Bravo Team Voice Channel")
    await team_ops_category.create_voice_channel("Support Team Voice Channel")
    
    await ctx.send("Server layout has been set up successfully!")

# Add more server setup functions as needed