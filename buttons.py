import discord

from embeds import eq2,eq3,eq4,eq5
from users import User


class master_button(discord.ui.View):
    iter = 2
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user
        self.right = None

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def b1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f"Неправильный ответ. правильный ответ  был: {self.right}", embed=eq[master_button.iter], view=bq[master_button.iter](user=self.user))

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def b2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f"Неправильный ответ. правильный ответ был: {self.right}", embed=eq[master_button.iter], view=bq[master_button.iter](user=self.user))

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def b3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f"Неправильный ответ. правильный ответ был: {self.right}", embed=eq[master_button.iter], view=bq[master_button.iter](user=self.user))

class bq1(master_button):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout,user=user)
        self.user = user

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def b2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq2, view=bq2(user=self.user))


class bq2(master_button):
    def __init__(self, *, timeout = 180, user: User):
        master_button.iter+=1
        super().__init__(timeout=timeout,user=user)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def b1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq3, view=bq3(user=self.user))

class bq3(master_button):
    def __init__(self, *, timeout = 180, user: User):
        master_button.iter+=1
        super().__init__(timeout=timeout,user=user)
        self.user = user

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def b2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq4, view=bq4(user=self.user))


class bq4(master_button):
    def __init__(self, *, timeout = 180, user: User):
        master_button.iter+=1
        super().__init__(timeout=timeout,user=user)
        self.user = user

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def b3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await interaction.response.edit_message(content="Правильный ответ!", embed=eq5, view=bq5(user=self.user))


class bq5(discord.ui.View):
    def __init__(self, *, timeout = 180, user: User):
        super().__init__(timeout=timeout)
        self.user = user

    @discord.ui.button(label='A', style=discord.ButtonStyle.secondary)
    async def b1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.user.right_answer()
        await self.user.quizresult(interaction=interaction)

    @discord.ui.button(label='B', style=discord.ButtonStyle.secondary)
    async def b2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.quizresult(interaction=interaction)

    @discord.ui.button(label='C', style=discord.ButtonStyle.secondary)
    async def b3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.quizresult(interaction=interaction)


bq = {2: bq2,
      3: bq3,
      4: bq4,
      5: bq5,}

eq = {2: eq2,
      3: eq3,
      4: eq4,
      5: eq5,}