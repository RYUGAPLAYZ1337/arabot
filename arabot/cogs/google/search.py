from urllib.parse import quote_plus

from aiohttp import ClientSession
from arabot.core import Category, Cog, Context
from arabot.core.utils import bold
from disnake import Embed
from disnake.ext.commands import command


class GoogleSearch(Cog, category=Category.LOOKUP, keys={"g_search_key", "g_cse"}):
    GSEARCH_BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, session: ClientSession):
        self.session = session

    @command(aliases=["g"], brief="Top Google Search result")
    async def google(self, ctx: Context, *, query):
        json = await self.session.fetch_json(
            self.GSEARCH_BASE_URL,
            params={
                "key": self.g_search_key,
                "cx": self.g_cse,
                "q": query,
                "num": 1,
            },
        )
        await ctx.reply(json["items"][0]["link"] if json.get("items") else "No results found")

    @command(aliases=["g3"], brief="Top 3 Google Search results")
    async def google3(self, ctx: Context, *, query):
        data = await self.session.fetch_json(
            self.GSEARCH_BASE_URL,
            params={
                "key": self.g_search_key,
                "cx": self.g_cse,
                "q": query,
                "num": 3,
            },
        )

        if not data.get("items"):
            await ctx.reply("No results found")
            return

        embed = Embed(
            title="Google search results",
            description="Showing top 3 search results",
            url=f"https://google.com/search?q={quote_plus(query)}",
        )

        for hit in data["items"]:
            embed.add_field(
                hit["link"],
                f"{bold(hit['title'])}\n{hit['snippet']}",
                inline=False,
            )
        await ctx.reply(embed=embed)