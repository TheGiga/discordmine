import random
import uuid

import discord
from discord.ui import Item
import config
from lib import User
from lib.database import db_session


class UpgradePickaxe(discord.ui.Button):
    def __init__(self, author_id: int, label: str, cost: int):
        super().__init__()
        self.author_id = author_id
        self.label = label
        self.cost = cost
        self.emoji = "⛏"

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.guild is None:
            return

        if interaction.user.id != self.author_id:
            return await interaction.response.send_message(
                ephemeral=True, content=":x: Its not your profile!"
            )

        user = await User.get_or_create(interaction.user)

        if user.total < self.cost:
            return await interaction.response.send_message(
                ephemeral=True, content=f":x: **You can't afford this.**\nYou need `{self.cost}` {config.STONE}"
            )

        user.pickaxe_level += 1
        user.total -= self.cost
        db_session.commit()

        new_view = discord.ui.View()
        new_view.add_item(discord.ui.Button(
            style=discord.ButtonStyle.green,
            label=self.label,
            disabled=True,
            emoji="☑"
        ))

        await interaction.message.edit(view=new_view)

        await interaction.response.send_message(
            ephemeral=True,
            content=f'**Your pickaxe is successfully upgraded.**\nNew level is `{user.pickaxe_level}`'
        )


class Upgrader(discord.ui.View):
    def __init__(self, author_id: int, label: str, cost: int, *items: Item):
        super().__init__(*items)
        self.add_item(UpgradePickaxe(author_id=author_id, label=label, cost=cost))

