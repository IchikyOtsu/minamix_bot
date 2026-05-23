import discord


class ExpiringView(discord.ui.View):
    def __init__(self, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.message: discord.Message | None = None

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.edit(
                    content="⏱️ Cette sélection a expiré.",
                    embed=None,
                    view=None,
                )
            except Exception:
                pass
