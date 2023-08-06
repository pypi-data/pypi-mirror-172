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
        self.children[0].disabled = True
        if len(pages) == 1: self.children[-1].disabled = True

    async def update(self,page:int):
        self.current_page = page
        if page==0: 
            self.children[0].disabled = True
            #self.children[1].disabled = True
            self.children[-1].disabled = False
            #self.children[-2].disabled = False
        elif page==self.length: 
            self.children[0].disabled = False
            #self.children[1].disabled = False
            self.children[-1].disabled = True
            #self.children[-2].disabled = True
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
                
    #@ui.button(label = 'before fast', style=discord.ButtonStyle.blurple)
    #async def first_page(self, interaction, button):
        #await self.show_page(0,interaction)

    @ui.button(label = "ᐊ", style=discord.ButtonStyle.grey)
    async def before_page(self, interaction, button):
        await self.show_page(self.current_page - 1,interaction)

    @ui.button(label='🗑️', style=discord.ButtonStyle.red)
    async def stop_page(self, interaction, button):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @ui.button(label='ᐅ', style=discord.ButtonStyle.grey)
    async def next_page(self, interaction, button):
        await self.show_page(self.current_page + 1,interaction)
	
    #@ui.button(label='next fast', style=discord.ButtonStyle.blurple)
    #async def last_page(self, interaction, button):
        #await self.show_page(self.length,interaction)
        
    
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