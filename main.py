import asyncio
import logging
import sys
import aiogram
import aiohttp

from config import bot, dp
from aiogram import types

from datetime import datetime
from bs4 import BeautifulSoup

@dp.message()
async def get_news(message: types.Message):
	await message.answer("Fetching news...")
	if not isinstance(message.text, str):
		await message.answer("Invalid input.")
		return
	query = message.text.replace(' ', '+')
	date = datetime.now().strftime("%Y%m%d")
	url = f"https://dzen.ru/news/search?text={query}+date%3A{date}"
	print(url)
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			if resp.status == 200:
				print(text := await resp.text())
				soup = BeautifulSoup(text, "html.parser")
				headers = [
					div.get_text(strip=True)
					for div in soup.find_all("div")
				]
				print(soup.find_all("div"))
				if headers:
					await message.answer("Top news headers:\n" + "\n".join(headers[:5]))
				else:
					await message.answer("No news headers found.")
			else:
				await message.answer("Failed to fetch news.")

async def main() -> None:
    await dp.start_polling(bot)


async def get_session_response():
	url = f"https://dzen.ru/news/search?text=спорт"
	print(url)
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			if resp.status == 200:
				print(resp)
				print(f"Here are the search results:\n{url}")
			else:
				print("Failed to fetch news.")

if __name__ == "__main__":
	# asyncio.run(get_session_response())
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())