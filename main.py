import asyncio
from crawl4ai import *
from urllib.parse import urlparse


url =  url = input("Enter the website URL: ").strip()
async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        print(result.markdown)
        
    domain = urlparse(url).netloc.replace("www.", "")
    filename = f"{domain}.txt"
    with open(filename, "w", encoding="utf-8") as f:
            f.write(result.markdown)

    print(f"\n✅ Scraped content saved to '{filename}'")

if __name__ == "__main__":
    asyncio.run(main())