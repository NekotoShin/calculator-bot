import os

import discord
from discord.ext import commands

from calculator import CalculatorView


class CalculatorCog(commands.Cog):
    def __init__(self, bot: discord.AutoShardedBot):
        self.bot = bot

    @discord.slash_command(description="Open the calculator.")
    async def calculator(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        msg = await ctx.respond("Preparing calculator...")
        embed = discord.Embed(description=f"```{'0'.rjust(30)}```", color=discord.Color.blurple())
        await msg.edit(content="", embed=embed, view=CalculatorView(ctx.author.id, self.bot))


class CalculatorBot(discord.AutoShardedBot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            activity=discord.Game("calculator")
        )
        self.add_cog(CalculatorCog(self))
        self._client_ready = False
        
    async def on_ready(self):
        if not self._client_ready:
            self._client_ready = True
            
            print(f"Logged in as {self.user.name}#{self.user.discriminator}")
            
    def run(self):
        super().run(
            os.environ["token"]
        )
        

if __name__ == "__main__":
    bot = CalculatorBot()
    bot.run()