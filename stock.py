import requests
from bs4 import BeautifulSoup
import asyncio
import telegram


async def send_message(ticker, company_name, latest_update, closing_price, previous_close):
    bot = telegram.Bot(token="5970479672:AAH17INZd_4NvnrIj221zZzUSwk7kOxpp6M")
    chat_id = "962648693"
    message = f"Company Name: {company_name}\nTicker: {ticker}\nLatest Update: {latest_update}\nClosing Price: {closing_price}\nPrevious Close: {previous_close}"
    await bot.send_message(chat_id=chat_id, text=message)

def get_data(ticker):
    url = f"https://www.marketwatch.com/investing/stock/{ticker}?countrycode=lk"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    company_name_el = soup.select_one("h1.company__name")
    company_name = company_name_el.text.strip()

    latest_update_el = soup.select_one("span.timestamp__time")
    latest_update = latest_update_el.text.strip()

    closing_price_el = soup.select_one("h2.intraday__price span.value")
    closing_price = closing_price_el.text.strip()

    previous_close_el = soup.select_one("td.u-semi")
    previous_close = previous_close_el.text.strip()

    return company_name, latest_update, closing_price, previous_close

async def main():
    tickers = ["odel.n0000", "ahpl.n0000"]
    tasks = []
    for ticker in tickers:
        data = get_data(ticker)
        company_name, latest_update, closing_price, previous_close = data
        task = asyncio.create_task(send_message(ticker, company_name, latest_update, closing_price, previous_close))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
