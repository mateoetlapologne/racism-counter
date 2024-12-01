import discord
from discord.ext import commands

# Intents nécessaires pour lire les messages et le contenu des messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Liste des mots à suivre
tracked_words = ["negro", "nigger", "nigga", "sale juif", "bougnoule", "sale noir", "sal arabe", "nigga", "négro"]  # Remplacez par vos mots
word_count = {word: 0 for word in tracked_words}  # Compteur pour chaque mot
user_count = {}  # Compteur des utilisateurs

# ID du salon où afficher l'embed (remplacez par l'ID réel)
TRACKER_CHANNEL_ID = 1211757745871790182


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

    # Envoi initial de l'embed dans le salon spécifié
    channel = bot.get_channel(TRACKER_CHANNEL_ID)
    if channel is None:
        print(f"Salon avec ID {TRACKER_CHANNEL_ID} introuvable.")
        return

    embed = discord.Embed(
        title="Qui est le plus raciste ?",
        color=discord.Color.blue()
    )
    embed.add_field(name="Les plus gros racelards", value="Aucune activité détectée.", inline=False)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmYNQiae8EaIvjRu69OjTmpXJa8KrsPGda7w&s")
    bot.embed_message = await channel.send(embed=embed)


@bot.event
async def on_message(message):
    # Ignore les messages envoyés par le bot lui-même
    if message.author.bot:
        return

    global user_count

    # Vérifie si le message contient un des mots suivis
    updated_words = False
    updated_users = False

    for word in tracked_words:
        if word in message.content.lower():
            word_count[word] += 1
            updated_words = True

            # Compteur utilisateur
            user = message.author
            if user not in user_count:
                user_count[user] = 0
            user_count[user] += 1
            updated_users = True

    if updated_words or updated_users:
        # Mettre à jour l'embed
        embed = discord.Embed(
            title="Racisme Tracker",
            color=discord.Color.blue()
        )

        # Ajoute les données de suivi des mots
        words_summary = "\n".join([f"{word} : {count} occurrence(s)" for word, count in word_count.items()])
        embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmYNQiae8EaIvjRu69OjTmpXJa8KrsPGda7w&s")
        

        # Ajoute les données des top utilisateurs
        top_users = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:5]
        users_summary = "\n".join([f"{user.name} : {count} mot(s)" for user, count in top_users])
        if not users_summary:
            users_summary = "Aucune activité détectée."
        embed.add_field(name="Les mecs les plus raciste", value=users_summary, inline=False)

        # Mettre à jour le message existant
        channel = bot.get_channel(TRACKER_CHANNEL_ID)
        if channel and hasattr(bot, 'embed_message') and bot.embed_message:
            await bot.embed_message.edit(embed=embed)
        else:
            print("Embed initial non trouvé ou canal inaccessible.")


# Lancement du bot avec le token

bot.run("")
