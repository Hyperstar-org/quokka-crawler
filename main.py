import asyncio, logging
from src.main import main


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('apify_client')

async def run_forever():
    while True:
        try:
            await main()
        except Exception as e:
            logger.info(f"Error during main(): {e}")
        logger.info("Sleeping for 4 hours before restarting...")
        await asyncio.sleep(4 * 60 * 60)

if __name__ == '__main__':
    asyncio.run(run_forever())
