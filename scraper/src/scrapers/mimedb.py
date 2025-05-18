import logging
import os
import re
import sys
import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SQLAlchemySession

SCRAPER_SRC_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRAPER_SRC_ROOT))
sys.path.insert(0, PROJECT_ROOT)
try:
    from backend.app.models.bacteria import Bacteria
except ImportError:
    logging.error(
        "Could not import backend.app.models.Bacteria. Scraper save will be problematic."
    )
    Bacteria = None


logger = logging.getLogger(__name__)


class MimeDBScraper:
    BASE_URL = "https://mimedb.org"
    MICROBES_URL = f"{BASE_URL}/microbes"

    def __init__(
        self,
        db_session: SQLAlchemySession,
        delay: float = 2.0,
        user_agent: Optional[str] = None,
    ):
        self.db_session = db_session
        self.delay = delay
        self.headers = {
            "User-Agent": user_agent
            or os.getenv("SCRAPER_USER_AGENT", "GenericScraper/1.0"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    def _get_page_content(self, url: str, retries: int = 3) -> Optional[str]:
        for attempt in range(retries):
            try:
                time.sleep(self.delay * attempt)
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"Request to {url} failed (attempt {attempt + 1}/{retries}): {e}"
                )
        logger.error(f"Failed to fetch {url} after {retries} attempts.")
        return None

    def get_bacteria_ids(self, max_pages: int = 1) -> List[str]:
        ids = []
        for page_num in range(1, max_pages + 1):
            page_url = f"{self.MICROBES_URL}?page={page_num}"
            logger.info(f"Fetching bacteria IDs from: {page_url}")
            html = self._get_page_content(page_url)
            if not html:
                continue

            soup = BeautifulSoup(html, "lxml")
            links = soup.select("td.microbe-link a.btn-card")
            if not links and page_num == 1:
                logger.warning(
                    "No bacteria links found on first page using selector 'td.microbe-link a.btn-card'. Check website structure."
                )
            page_ids_found = 0
            for link in links:
                href = link.get("href")
                if href and "/microbes/" in href:
                    bacteria_id = href.split("/microbes/")[-1]
                    if bacteria_id.startswith("MMDBm"):
                        ids.append(bacteria_id)
                        page_ids_found += 1
            if page_ids_found == 0 and page_num > 1:
                logger.info(
                    f"No more IDs found on page {page_num}. Stopping ID collection."
                )
                break
        return list(set(ids))

    def scrape_bacteria_data(self, bacteria_id: str) -> Optional[Dict]:
        detail_url = f"{self.BASE_URL}/microbes/{bacteria_id}"
        logger.info(f"Scraping details for {bacteria_id} from {detail_url}")
        html = self._get_page_content(detail_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        data = {"bacteria_id": bacteria_id}

        title_el = soup.select_one(".page-header h1")
        if title_el:
            name_match = re.match(r"^(.*?) \(MMDBm\d+\)", title_el.text.strip())
            data["name"] = (
                name_match.group(1).strip() if name_match else title_el.text.strip()
            )

        tax_map = {
            "Superkingdom": "superkingdom",
            "Kingdom": "kingdom",
            "Phylum": "phylum",
            "Class": "class_name",
            "Order": "order",
            "Family": "family",
            "Genus": "genus",
            "Species": "species",
            "Strain": "strain",
        }
        for row in soup.select("#taxinfo tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td and th.text.strip() in tax_map:
                data[tax_map[th.text.strip()]] = (
                    td.text.strip() if "Not Available" not in td.text else None
                )

        prop_map = {
            "Gram staining properties": "gram_stain",
            "Shape": "shape",
            "Mobility": "mobility",
            "Flagellar presence": "flagellar_presence",
            "Number of membranes": "number_of_membranes",
            "Oxygen preference": "oxygen_preference",
            "Optimal temperature": "optimal_temperature",
            "Temperature range": "temperature_range",
            "Habitat": "habitat",
            "Biotic relationship": "biotic_relationship",
            "Cell arrangement": "cell_arrangement",
            "Sporulation": "sporulation",
            "Metabolism": "metabolism",
            "Energy source": "energy_source",
        }
        for row in soup.select("#microbe-properties tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td and th.text.strip() in prop_map:
                field_name = prop_map[th.text.strip()]
                value = td.text.strip()
                if "Not Available" in value:
                    value = None

                if field_name in ["mobility", "flagellar_presence", "sporulation"]:
                    data[field_name] = value.lower() == "yes" if value else None
                elif field_name == "optimal_temperature" and value:
                    match = re.search(r"(\d+(\.\d+)?)", value)
                    data[field_name] = float(match.group(1)) if match else None
                else:
                    data[field_name] = value

        disease_el = soup.select_one("td.microbe-disease")
        if disease_el:
            path_text = disease_el.text.strip().lower()
            if "non-pathogenic" in path_text:
                data["is_pathogen"] = False
            elif "pathogenic" in path_text:
                data["is_pathogen"] = True
            else:
                data["is_pathogen"] = False

        return data

    def save_bacteria_data(self, data: Dict) -> bool:
        if not Bacteria:
            logger.error("Bacteria model not available. Cannot save to DB.")
            return False
        if "bacteria_id" not in data:
            logger.error(
                f"Missing bacteria_id in data: {data.get('name')}. Cannot save."
            )
            return False

        try:
            existing = (
                self.db_session.query(Bacteria)
                .filter_by(bacteria_id=data["bacteria_id"])
                .first()
            )
            if existing:
                logger.info(f"Updating existing bacteria: {data['bacteria_id']}")
                for key, value in data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
            else:
                logger.info(f"Creating new bacteria: {data['bacteria_id']}")
                valid_keys = {column.name for column in Bacteria.__table__.columns}
                filtered_data = {k: v for k, v in data.items() if k in valid_keys}
                db_bacteria = Bacteria(**filtered_data)
                self.db_session.add(db_bacteria)

            self.db_session.commit()
            return True
        except IntegrityError:
            self.db_session.rollback()
            logger.warning(
                f"Integrity error for {data['bacteria_id']} (likely duplicate if create race). Skipping."
            )
            return False
        except Exception as e:
            self.db_session.rollback()
            logger.error(
                f"Error saving bacteria {data.get('bacteria_id')}: {e}", exc_info=True
            )
            return False
