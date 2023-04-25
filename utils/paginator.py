import discord
from typing import List
from collections import deque


class PaginationView(discord.ui.View):

    def __init__(self, embeds: List[discord.Embed], author: None) -> None:
        super().__init__(timeout=None)

        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self._author = author

    async def update_buttons(self, interaction: discord.Interaction) -> None:
        self._queue[0].set_footer(
            text=f'Pages of {self._current_page}/{self._len}')
        if self._current_page == self._len:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        if self._current_page == 1:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        await interaction.edit_original_response(view=self)

    @discord.ui.button(emoji='⬅️')
    async def previouts(self, interaction: discord.Interaction, _):
        if interaction.user.id == self._author:
            self._queue.rotate(-1)
            embed = self._queue[0]
            self._current_page -= 1
            await interaction.response.edit_message(embed=embed)
            await self.update_buttons(interaction)
        else:
            await interaction.response.send_message(
                'У вас нет прав на изменения данной страницы. Используйте /publics повторно',
                ephemeral=True)

    @discord.ui.button(emoji='➡️')
    async def next(self, interaction: discord.Interaction, _):
        if interaction.user.id == self._author:
            self._queue.rotate(1)
            embed = self._queue[0]
            self._current_page += 1
            await interaction.response.edit_message(embed=embed)
            await self.update_buttons(interaction)
        else:
            await interaction.response.send_message(
                'У вас нет прав на изменения данной страницы. Используйте /publics повторно',
                ephemeral=True)

    @property
    def initial(self) -> discord.Embed:
        return self._initial