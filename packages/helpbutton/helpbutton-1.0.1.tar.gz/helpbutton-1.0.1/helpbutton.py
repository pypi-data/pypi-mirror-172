from discord.ui import View
from discord import ui
import discord
from typing import Optional,List

class get(View):
    def __init__(self,pages:list,timeout:float,user:Optional[discord.Member]=None) -> None:
        super().__init__(timeout=timeout)
        self.pages = pages
        self.current_page = 0
        self.length = len(pages)-1
        self.user=user
        self.children[0].disabled,self.children[1].disabled = True,True

    async def update(self,page:int):
        self.current_page = page
        if page==0: 
            self.children[0].disabled = True
            self.children[1].disabled = True
            self.children[-1].disabled = False
            self.children[-2].disabled = False
        elif page==self.length: 
            self.children[0].disabled = False
            self.children[1].disabled = False
            self.children[-1].disabled = True
            self.children[-2].disabled = True
        else: 
            for i in self.children: i.disabled=False

    async def show_page(self,page:int,interaction:discord.Interaction=None):
        await self.update(page)
        content,embeds,files = await self.getPage(self.pages[page])
        
        await interaction.response.edit_message(
            content=content,
            embeds= embeds,
            attachments= files or [],
            view=self
        )

    async def getPage(self,page):
        if isinstance(page, str):
            return page, [], []
        elif isinstance(page, discord.Embed):
            return None, [page], []
        elif isinstance(page, discord.File):
            return None, [], [page]
        elif isinstance(page, List):
            if all(isinstance(x, discord.Embed) for x in page):
                return None,page,[]
            if all(isinstance(x, discord.File) for x in page):
                return None, [], page
            else:
                raise TypeError("Can't have alternative files and embeds (please keep the type same)")

    @ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
    async def first_page(self, interaction, button):
        await self.show_page(0,interaction)

    @ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.green)
    async def before_page(self, interaction, button):
        await self.show_page(self.current_page - 1,interaction)

    @ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.red)
    async def stop_page(self, interaction, button):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.green)
    async def next_page(self, interaction, button):
        await self.show_page(self.current_page + 1,interaction)

    @ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
    async def last_page(self, interaction, button):
        await self.show_page(self.length,interaction)
    
    async def interaction_check(self, interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message(
                    "This command is for someone else",
                    ephemeral=True,
                )
                return False
        return True

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled=True
        self.stop()