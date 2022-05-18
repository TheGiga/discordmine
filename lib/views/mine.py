import random
import uuid

import discord
from discord.ui import Item
import config
from lib import User, generate_random_field
from lib.database import db_session


class Miner(discord.ui.View):
    def __init__(self, author_id: int, *items: Item):
        super().__init__(*items)
        self.author_id = author_id

    @discord.ui.button(label="Pick!", style=discord.ButtonStyle.gray, emoji="⛏", custom_id=str(uuid.uuid4()))
    async def miner_counter(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.guild is None:
            return

        if interaction.user.id != self.author_id:
            return await interaction.response.send_message(
                ephemeral=True, content=":x: Its not your mine or someone stole it. **Use `/mine`**"
            )

        rng = random.randint(1, 100)
        if rng < 3:
            broken_pick_view = discord.ui.View()
            broken_pick_view.add_item(discord.ui.Button(
                disabled=True, label='Oops, your pickaxe broke.', emoji="😳", style=discord.ButtonStyle.red
            ))
            await interaction.response.edit_message(
                content=interaction.message.content,
                view=broken_pick_view,
            )
            return await interaction.message.delete(delay=6)
        elif rng > 90:
            self.children[1].__setattr__("disabled", False)  # making TNT button enabled

        user = await User.get_or_create(interaction.user)
        to_add = 1 * user.pickaxe_level
        user.total += to_add
        db_session.commit()

        content = await generate_random_field(from_existing=interaction.message)

        try:
            await interaction.response.edit_message(content=content, view=self)
        except discord.NotFound:
            return

    @discord.ui.button(
        label="TNT Ready!", style=discord.ButtonStyle.red, emoji=config.TNT, custom_id=str(uuid.uuid4()),
        disabled=True
    )
    async def tnt_explosion(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.guild is None:
            return

        if interaction.user.id != self.author_id:
            return await interaction.response.send_message(
                ephemeral=True, content=":x: Its not your mine or someone stole it. **Use `/mine`**"
            )

        self.children[1].__setattr__("disabled", True)

        user = await User.get_or_create(interaction.user)
        to_add = 5 * user.pickaxe_level
        user.total += to_add
        db_session.commit()

        content = await generate_random_field()

        try:
            await interaction.message.edit(content=content, view=self)
            await interaction.response.send_message(
                ephemeral=True,
                content=f"{config.TNT} Your TNT blew up and gave you `{to_add}` blocks!"
            )
        except discord.NotFound:
            return
