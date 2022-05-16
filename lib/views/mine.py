import random

import discord
from discord.ui import Item

from lib import User, generate_random_field
from lib.database import db_session


class Miner(discord.ui.View):
    def __init__(self, author: discord.Member, *items: Item):
        super().__init__(*items)
        self.author = author

    @discord.ui.button(label="Pick!", style=discord.ButtonStyle.gray, emoji="⛏")
    async def miner_counter(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.guild is None:
            return

        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(ephemeral=True, content=":x: Its not your mine, use `/mine`")

        broke = random.randint(1, 100)
        print(broke)
        if broke < 3:
            return await interaction.response.edit_message(
                content="😳 Oops, your pickaxe broke, use `/mine` to start again.",
                view=None
            )

        user = await User.get_or_create(interaction.user)
        user.total += 1
        db_session.commit()

        content = await generate_random_field(from_existing=interaction.message)

        await interaction.response.edit_message(content=content, view=self)
