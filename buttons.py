import discord

from embeds import eq2,eq3,eq4,eq5
from users import User

class bq1(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def bq11(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ  был: B", embed=eq2, view=bq2(user=self.user))

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def bq12(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq2, view=bq2(user=self.user))

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def bq13(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ был: B", embed=eq2, view=bq2(user=self.user))



class bq2(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def bq21(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq3, view=bq3(user=self.user))

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def bq22(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ был: А", embed=eq3, view=bq3(user=self.user))

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def bq23(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ был: А", embed=eq3, view=bq3(user=self.user))



class bq3(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def bq31(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ  был: B", embed=eq4, view=bq4(user=self.user))

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def bq32(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq4, view=bq4(user=self.user))

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def bq33(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ  был: B", embed=eq4, view=bq4(user=self.user))



class bq4(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def bq41(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ был: C", embed=eq5, view=bq5(user=self.user))

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def bq42(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Неправильный ответ. правильный ответ был: C", embed=eq5, view=bq5(user=self.user))

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def bq43(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq5, view=bq5(user=self.user))



class bq5(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def bq51(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await self.user.quizresult(interaction=interaction)
    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def bq52(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.quizresult(interaction=interaction)
    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def bq53(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.quizresult(interaction=interaction)