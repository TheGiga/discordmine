import random
import discord

import config


def render(field: str) -> str:  # rendering field to player textures
    new_field = field.replace("🟦", config.DIAMOND)
    new_field = new_field.replace("🟨", config.GOLD)
    new_field = new_field.replace("⬜", config.IRON)
    new_field = new_field.replace("🔳", config.COAL)
    new_field = new_field.replace("🟫", config.STONE)
    new_field = new_field.replace("🟧", config.DEEPSLATE)
    new_field = new_field.replace("😳", config.CHARACTER)

    return new_field


def un_render(field: str) -> str:  # un-rendering field to dev textures
    new_field = field.replace(config.DIAMOND, "🟦")
    new_field = new_field.replace(config.GOLD, "🟨")
    new_field = new_field.replace(config.IRON, "⬜")
    new_field = new_field.replace(config.COAL, "🔳")
    new_field = new_field.replace(config.STONE, "🟫")
    new_field = new_field.replace(config.DEEPSLATE, "🟧")
    new_field = new_field.replace(config.CHARACTER, "😳")

    return new_field


DEV_BALANCED_LIST = \
    ["🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🔳", "🔳", "🔳", "🔳", "⬜", "⬜", "⬜", "🟨", "🟨", "🟦"]


async def generate_random_field(from_existing: discord.Message = None) -> str:
    def r():
        return random.choice(DEV_BALANCED_LIST)

    # if field was already created from main command, this code will generate new blocks in front, and move old ones
    if from_existing is not None:
        ex = un_render(from_existing.clean_content.__str__())
        line2 = f"{ex[7]}{ex[8]}{ex[9]}{ex[10]}{r()}"
        main = f'{config.VOID}{config.VOID}{config.CHARACTER}{ex[16]}{r()}'
        line4 = f"{ex[19]}{ex[20]}{ex[21]}{ex[22]}{r()}"
    else:  # just creating field
        line2 = f"{r()}{r()}{r()}{r()}{r()}"
        main = f"{config.VOID}{config.VOID}{config.CHARACTER}{r()}{r()}"
        line4 = f"{r()}{r()}{r()}{r()}{r()}"

    stone = f"{config.STONE}{config.STONE}{config.STONE}{config.STONE}{config.STONE}"
    deepslate = f"{config.DEEPSLATE}{config.DEEPSLATE}{config.DEEPSLATE}{config.DEEPSLATE}{config.DEEPSLATE}"

    return render(f"{stone}\n{line2}\n{main}\n{line4}\n{deepslate}")
