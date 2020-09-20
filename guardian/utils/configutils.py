import discord


async def add_to_config(ctx, string_to_add: str, command_list, command: str):
    """
    :param self:
    :param ctx: command context
    :param string_to_add: string to be added to the command's list
    :param command_list: list that the string will be added to
    :param command: command that that executed this function
    """

    try:

        cl = await command_list()
        commandlist = cl

        if string_to_add in commandlist:
            async with command_list() as command_list:
                command_list.remove(string_to_add)

            removeembed = discord.Embed(title="Guardian", color=0xff0080)
            removeembed.set_thumbnail(url=ctx.guild.icon_url)
            removeembed.add_field(name=f"Removed {command} filter", value=string_to_add)
            await ctx.send(embed=removeembed)

        else:
            async with command_list() as command_list:
                command_list.append(string_to_add)

            addembed = discord.Embed(title="Guardian", color=0xff0080)
            addembed.set_thumbnail(url=ctx.guild.icon_url)
            addembed.add_field(name=f"Added new {command} filter", value=string_to_add)
            await ctx.send(embed=addembed)

    except Exception as exception:
        error_string = f"There was an exception executing the {command}, error returned: {exception}"
        print(error_string)
        await ctx.send(error_string)
