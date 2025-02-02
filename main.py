import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Word list to track
tracked_words = ["negro", "nigger", "nigga", "sale juif", "bougnoule", "sale noir", "sal arabe", "nigga", "négro"]  # Change, remove or add words as u want
word_count = {word: 0 for word in tracked_words}
user_count = {}

# CHANNEL ID FOR SHOW THE EMBED
TRACKER_CHANNEL_ID = 1211757745871790182 #example
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    channel = bot.get_channel(TRACKER_CHANNEL_ID)
    if channel is None:
        print(f"Salon avec ID {TRACKER_CHANNEL_ID} introuvable.")
        return
    embed = discord.Embed(
        title="Who is racist",
        color=discord.Color.blue()
    )
    embed.add_field(name="Who is racist", value="no activity", inline=False)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmYNQiae8EaIvjRu69OjTmpXJa8KrsPGda7w&s")
    bot.embed_message = await channel.send(embed=embed)
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    global user_count
    updated_words = False
    updated_users = False
    for word in tracked_words:
        if word in message.content.lower():
            word_count[word] += 1
            updated_words = True
            user = message.author
            if user not in user_count:
                user_count[user] = 0
            user_count[user] += 1
            updated_users = True
    if updated_words or updated_users:
        embed = discord.Embed(
            title="Racisme Tracker",
            color=discord.Color.blue()
        )
        words_summary = "\n".join([f"{word} : {count} occurrence(s)" for word, count in word_count.items()])
        embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmYNQiae8EaIvjRu69OjTmpXJa8KrsPGda7w&s")
        top_users = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:5]
        users_summary = "\n".join([f"{user.name} : {count} mot(s)" for user, count in top_users])
        if not users_summary:
            users_summary = "No activity"
        embed.add_field(name="Raciest people", value=users_summary, inline=False)
        channel = bot.get_channel(TRACKER_CHANNEL_ID)
        if channel and hasattr(bot, 'embed_message') and bot.embed_message:
            await bot.embed_message.edit(embed=embed)
        else:
            print("Embed not found or incorrect channel id")


# Lancement du bot avec le token

bot.run("")
