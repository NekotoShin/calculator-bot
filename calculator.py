import discord
import operator


class CalculatorView(discord.ui.View):
    op_dict = {
        "+": operator.add,
        "-": operator.sub,
        "×": operator.mul,
        "÷": operator.truediv
    }
    
    def __init__(self, author_id: int, bot: discord.AutoShardedBot):
        super().__init__()
        self.author_id = author_id
        self.bot = bot
        self.result = self.last = "0"
        self.operator = None
        self.clear_next = False

    async def edit_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=f"```{self.result.rjust(30)}```",
            color=discord.Color.blurple()
        )
        await interaction.response.edit_message(embed=embed)

    async def handle_number(self, button: discord.Button, interaction: discord.Interaction):
        number = button.label
        if self.clear_next or self.result == "0":
            self.clear_next = False
            self.result = number
        else:
            self.result += number
        await self.edit_embed(interaction)

    async def handle_operator(self, button: discord.Button, interaction: discord.Interaction):
        if self.operator is not None:
            op_func = self.op_dict[self.operator]
            result = op_func(float(self.last), float(self.result))
            self.last = str(round(result, 10)).strip("0").strip(".")
        else:
            self.last = self.result
        self.operator = button.label
        self.result = "0"
        await self.edit_embed(interaction)

    @discord.ui.button(label="AC", style=discord.ButtonStyle.danger, row=0)
    async def all_clear(self, button, interaction):
        self.result = "0"
        self.last = "0"
        self.operator = None
        await self.edit_embed(interaction)
    
    @discord.ui.button(label="C", style=discord.ButtonStyle.danger, row=0)
    async def clear(self, button, interaction):
        self.result = "0"
        await self.edit_embed(interaction)
    
    @discord.ui.button(label="←", style=discord.ButtonStyle.primary, row=0)
    async def backspace(self, button, interaction):
        if self.result != "0":
            self.result = self.result[:-1]
        if self.clear_next or self.result == "":
            self.result = "0"
        await self.edit_embed(interaction)
    
    @discord.ui.button(label="÷", style=discord.ButtonStyle.secondary, row=0)
    async def divide(self, button, interaction):
        await self.handle_operator(button, interaction)
    
    @discord.ui.button(label="1", style=discord.ButtonStyle.success, row=1)
    async def one(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="2", style=discord.ButtonStyle.success, row=1)
    async def two(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="3", style=discord.ButtonStyle.success, row=1)
    async def three(self, button, interaction):
        await self.handle_number(button, interaction)

    @discord.ui.button(label="×", style=discord.ButtonStyle.secondary, row=1)
    async def multiply(self, button, interaction):
        await self.handle_operator(button, interaction)
    
    @discord.ui.button(label="4", style=discord.ButtonStyle.success, row=2)
    async def four(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="5", style=discord.ButtonStyle.success, row=2)
    async def five(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="6", style=discord.ButtonStyle.success, row=2)
    async def six(self, button, interaction):
        await self.handle_number(button, interaction)

    @discord.ui.button(label="-", style=discord.ButtonStyle.secondary, row=2)
    async def subtract(self, button, interaction):
        await self.handle_operator(button, interaction)
    
    @discord.ui.button(label="7", style=discord.ButtonStyle.success, row=3)
    async def seven(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="8", style=discord.ButtonStyle.success, row=3)
    async def eight(self, button, interaction):
        await self.handle_number(button, interaction)
    
    @discord.ui.button(label="9", style=discord.ButtonStyle.success, row=3)
    async def nine(self, button, interaction):
        await self.handle_number(button, interaction)

    @discord.ui.button(label="+", style=discord.ButtonStyle.secondary, row=3)
    async def plus(self, button, interaction):
        await self.handle_operator(button, interaction)
    
    @discord.ui.button(label="+/-", style=discord.ButtonStyle.primary, row=4)
    async def negate(self, button, interaction):
        if self.result != "0":
            if self.result.startswith("-"):
                self.result = self.result[1:]
            else:
                self.result = f"-{self.result}"
        if self.clear_next:
            self.clear_next = False
        await self.edit_embed(interaction)
    
    @discord.ui.button(label="0", style=discord.ButtonStyle.success, row=4)
    async def zero(self, button, interaction):
        await self.handle_number(button, interaction)

    @discord.ui.button(label=".", style=discord.ButtonStyle.success, row=4)
    async def dot(self, button, interaction):
        if self.clear_next:
            self.result = "0."
            self.clear_next = False
        elif "." not in self.result:
            self.result = f"{self.result}."
        await self.edit_embed(interaction)
    
    @discord.ui.button(label="=", style=discord.ButtonStyle.primary, row=4)
    async def equal(self, button, interaction):
        if self.operator:
            op_func = self.op_dict[self.operator]
            result = op_func(float(self.last), float(self.result))
            self.result = str(round(result, 10)).strip("0").strip(".")
            self.last = "0"
            self.operator = None
            self.clear_next = True
        await self.edit_embed(interaction)

    @discord.ui.button(label="X", style=discord.ButtonStyle.danger, row=4)
    async def close(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content="Calculator closed.",
            embed=None,
            view=None,
            delete_after=3
        )
    
    async def interaction_check(self, interaction):
        return interaction.user.id == self.author_id
    
    async def on_check_failure(self, interaction):
        await interaction.response.send_message(
            "You are not the owner of this calculator.",
            ephemeral=True
        )