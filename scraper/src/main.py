import argparse
import logging
import sys
import time

from src.db import get_scraper_db
from src.scrapers.mimedb import MimeDBScraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("scraper_run.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)


def run_scraper(max_pages: int, max_bacteria_per_page: int, delay: float):
    logger.info(
        f"Starting MimeDB scrape: max_pages={max_pages}, max_bacteria_per_page={max_bacteria_per_page}, delay={delay}s"
    )

    db_session_gen = get_scraper_db()
    db = next(db_session_gen)

    scraper = MimeDBScraper(db_session=db, delay=delay)

    try:
        bacteria_ids = scraper.get_bacteria_ids(max_pages=max_pages)
        logger.info(f"Found {len(bacteria_ids)} bacteria IDs to process.")

        successful_scrapes = 0
        failed_scrapes = 0

        for i, bacteria_id in enumerate(bacteria_ids):
            if max_bacteria_per_page and i >= (max_pages * max_bacteria_per_page):
                logger.info(
                    f"Reached processing limit of {max_pages * max_bacteria_per_page} bacteria."
                )
                break

            logger.info(f"Processing ID {i + 1}/{len(bacteria_ids)}: {bacteria_id}")
            data = scraper.scrape_bacteria_data(bacteria_id)
            if data:
                if scraper.save_bacteria_data(data):
                    successful_scrapes += 1
                else:
                    failed_scrapes += 1
            else:
                failed_scrapes += 1
            time.sleep(0.1)

        logger.info(
            f"Scraping finished. Successful: {successful_scrapes}, Failed: {failed_scrapes}"
        )

    except Exception as e:
        logger.error(f"Scraper run failed: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MimeDB Bacteria Scraper")
    parser.add_argument(
        "--max-pages", type=int, default=1, help="Max list pages to scrape for IDs."
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=10,
        help="Max bacteria details to scrape per page (approx total items = max_pages * max_items).",
    )
    parser.add_argument(
        "--delay", type=float, default=2.0, help="Delay between HTTP requests."
    )

    args = parser.parse_args()

    run_scraper(
        max_pages=args.max_pages, max_bacteria_per_page=args.max_items, delay=args.delay
    )
