from RMPScraper import RMPScraper
import pytest

@pytest.fixture
def scraper():
    scraper = RMPScraper()
    yield scraper  # This is where the testing happens!
    del scraper



