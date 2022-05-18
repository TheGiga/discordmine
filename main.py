import os
import discord
from dotenv import load_dotenv
from sqlalchemy import desc

import config
import lib.views
from lib import User, generate_random_field
from lib.database import Base, engine, db_session

load_dotenv()  # .env is automatically loaded.

bot = discord.Bot(intents=discord.Intents.default())  # im not sure, but I think default intents is enough


@bot.event
async def on_ready():
    print(f'Registered {len(bot.commands)} commands')
    print(f"Discord Mine is running as user {bot.user}")


@bot.slash_command(name='mine', description="Work? Again? Augh...")
async def mine(ctx: discord.ApplicationContext):
    if ctx.guild is None:
        return await ctx.respond(content="This command can't be used in DM's.")

    await User.get_or_create(ctx.author)

    field = await generate_random_field()

    await ctx.respond(content=field, view=lib.views.Miner(author_id=ctx.author.id))


@bot.slash_command(name='leaders', description="User leaderboard by mined blocks.")
async def leaderboard(ctx: discord.ApplicationContext):
    query: [User] = (db_session.query(User).order_by(desc(User.total))).all()

    lb = ""
    i = 0
    for usr in query:
        if i == 10:
            break
        discord_instance = await bot.fetch_user(usr.discord_id)
        lb += f"**{i + 1}.** " \
              f"{str(discord_instance) if discord_instance is not None else usr.discord_id}" \
              f" - `{usr.total}` <:stone:975452400078966795>\n"
        i += 1

    embed = discord.Embed(description=lb, color=discord.Colour.embed_background())
    embed.title = "Top 10 users by mined blocks."
    embed.timestamp = discord.utils.utcnow()
    embed.set_footer(text='by gigalegit-#0880')

    await ctx.respond(embed=embed)


@bot.slash_command(name='profile', description='Check you profile and statisctics.')
async def profile(ctx: discord.ApplicationContext, member: discord.Member = None):
    if member is None:
        member = ctx.author

    usr: User = await User.get_or_create(member)

    embed = discord.Embed(
        title='Discord Mine',
        timestamp=discord.utils.utcnow(),
        colour=discord.Colour.embed_background()
    )
    embed.set_thumbnail(url='https://i.imgur.com/43tdQd9.png')

    embed.add_field(name=f"{config.STONE} Mined blocks", value=str(usr.total))
    embed.add_field(name='⛏ Pickaxe level', value=str(usr.pickaxe_level))

    embed.set_footer(text='by gigalegit-#0880')

    if member is not None:
        cost = 5000 * usr.pickaxe_level
        view = lib.views.Upgrader(label=f"Upgrade Pickaxe: {cost} stone", author_id=member.id, cost=cost)
    else:
        view = None

    await ctx.respond(view=view, embed=embed)


if __name__ == "__main__":
    from lib.models import *

    Base.metadata.create_all(bind=engine)

    bot.run(os.getenv("TOKEN"))
