from discord import Interaction, Embed
from src.utils.db import get_db_connection
from src.utils.wallet import modify_user_balance
from src.utils.format import format_amount
import random
import time
import discord

JOKES = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau !",
    "Quel est le comble d'un électricien ? De ne pas être au courant !",
    "Pourquoi les会计师 portent-ils des lunettes ? Parce qu'ils additionnent tout !",
    "Quel est le pain préféré des programmeurs ? Le pain bis (byte) !",
    "Pourquoi les poissons ne jouent-ils pas au poker ? Parce qu'il y a trop de requins !",
    "Quel est le comble d'un jardinier ? De ne pas savoir planter un clou !",
    "Pourquoi les informaticiens confondent-ils Halloween et Noël ? Parce que OCT 31 = DEC 25 !",
    "Quel est le comble d'un chauffard ? De prendre le train pour aller au travail !",
    "Pourquoi les oiseaux volent-ils en formation ? Pour payer moins de péage !",
    "Quel est le comble d'un couvreur ? De ne pas trouver le toit de sa maison !",
    "Pourquoi les grues sont-elles toujours fatiguées ? Parce qu'elles travaillent debout !",
    "Quel est le comble d'un boucher ? De ne pas avoir le cœur à l'ouvrage !",
    "Pourquoi les maçons portent-ils des ceintures ? Pour tenir les murs !",
    "Quel est le comble d'un astronome ? De ne pas voir plus loin que son nez !",
    "Pourquoi les boulangers sont-ils toujours de bonne humeur ? Parce que leur métier est pain !",
    "Quel est le comble d'un horloger ? De ne jamais avoir une minute à perdre !",
    "Pourquoi les pilotes de taxi sont-ils toujours pressés ? Parce qu'ils ont des courses à faire !",
    "Quel est le comble d'un bibliothécaire ? De ne pas savoir où ranger ses livres !",
    "Pourquoi les vetsrinaires ont-ils toujours des animaux autour d'eux ? Parce qu'ils adorent les bêtes !",
    "Quel est le comble d'un facteur ? De ne jamais avoir le temps de lire le courrier !",
    "Pourquoi les architectes dessinent-ils toujours en noir et blanc ? Pour faire économies de couleurs !",
    "Quel est le comble d'un pompier ? De ne pas trouver la sortie !",
    "Pourquoi les dentistes sont-ils toujours souriants ? Parce qu'ils travaillent à la chaîne !",
    "Quel est le comble d'un jardinier ? De ne pas savoir quel temps il fait !",
    "Pourquoi les avocats portent-ils des robes ? Parce que le costume c'est trop cher !",
    "Quel est le comble d'un joueur d'échecs ? De ne pas pouvoir caser sa reine !",
    "Pourquoi les médecins sont-ils toujours pressés ? Parce qu'ils ont des patients à voir !",
    "Quel est le comble d'un mécanicien ? De ne pas savoir réparer sa propre voiture !",
    "Pourquoi les photographes sont-ils toujours flous ? Parce qu'ils développent leur talent !",
    "Quel est le comble d'un directeur ? De ne pas avoir le temps de diriger !",
    "Pourquoi les程序员 mangent-ils des nouilles ? Parce qu'ils adorent le code !",
    "Quel est le comble d'un腰鼓手 ? De ne pas savoir percussion !",
    "Pourquoi les enseignants ont-ils des vacances ? Pour récupérer des élèves !",
    "Quel est le comble d'un踢足球运动员 ? De ne pas savoir où donner des coups de pied !",
    "Pourquoi les快递员 courent-ils toujours ? Pour ne pas rater leur tournée !",
    "Quel est le comble d'un科学家 ? De ne pas trouver la réponse !",
    "Pourquoi les厨师 portent-ils un chapeau ? Pour se couvrir la tête quand ils mijotent !",
    "Quel est le comble d'un画家 ? De ne pas voir les couleurs !",
    "Pourquoi les木匠 travail。他们总是敲敲打打！",
    "Quel est le comble d'un商人 ? De ne jamais avoir assez d'argent !",
    "Pourquoi les程序员 adorent-ils les bugs ? Parce qu'ils peuvent les corriger !",
    "Quel est le comble d'un会计 ? De toujours compter les sous !",
    "Pourquoi les律师总是赢得辩论？因为他们知道法律！",
    "Quel est le comble d'un画家 ? De ne jamais finir son œuvre !",
    "Pourquoi les木匠 mesurent-ils deux fois ? Pour ne pas se tromper !",
    "Quel est le comble d'un农民 ? De travailler à la sueur de son front !",
    "Pourquoi les快递员 connaissent-ils tous les chemins ? Parce qu'ils livrent partout !",
    "Quel est le comble d'un老师 ? De ne pas avoir la réponse !",
    "Pourquoi les程序员 utilisent-ils des raccourcis ? Pour aller plus vite !",
]

async def register(bot):
    @bot.tree.command(
        name="work",
        description="Travailler pour gagner de l'argent (utilisable 1x par semaine)."
    )
    async def work(interaction: Interaction):
        db = get_db_connection()
        cursor = db.cursor()
        user_id = interaction.user.id
        current_time = int(time.time())

        cursor.execute("SELECT last_work FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            last_work = result[0]
            if last_work is not None:
               
                if current_time - last_work < 604800:
               
                    remaining = 604800 - (current_time - last_work)
                    days = remaining // 86400
                    hours = (remaining % 86400) // 3600
                    minutes = (remaining % 3600) // 60

                    embed = Embed(
                        title="⏰ Cooldown actif",
                        description=f"Tu pourras travailler à nouveau dans **{days}j {hours}h {minutes}min**.",
                        color=discord.Color.orange()
                    )
                    embed.set_footer(text="Système d'économie")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    db.close()
                    return
        else:
         
            cursor.execute("INSERT INTO users (user_id, last_work) VALUES (%s, %s)", (user_id, 0))
            db.commit()

        gain = random.randint(50, 250)

        new_balance = await modify_user_balance(db, user_id, gain, "add")

        cursor.execute("UPDATE users SET last_work = %s WHERE user_id = %s", (current_time, user_id))
        db.commit()

        joke = random.choice(JOKES)

        embed = Embed(
            title="💼 Travail terminé !",
            description=f"Tu as gagné **{format_amount(gain)}💰** !\n\n**😄 Blague du jour :**\n_{joke}_\n\n📊 Nouveau solde : **{format_amount(new_balance)}💰**",
            color=discord.Color.green()
        )
        embed.set_footer(text="Prochain travail possible dans 1 semaine")
        await interaction.response.send_message(embed=embed, ephemeral=False)
        db.close()