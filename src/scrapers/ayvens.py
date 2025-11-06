import re
import sys
import time
from pathlib import Path
from decimal import Decimal
from dotenv import dotenv_values
from playwright.sync_api import sync_playwright
import nest_asyncio

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from configs.database import SessionLocal
from components.cars.models import Car

nest_asyncio.apply()

# config
config = dotenv_values(".env")

# playwright
pw = sync_playwright().start()


class AyvensScraper:
    BASE_URL = "https://usedcars.ayvens.com"
    CAR_LIST_URL = "/sv-se/bilar/tesla/model-31+model-32+model-y1+model-y2"
    SKIP_EXISTING_CARS = True

    def __init__(self):
        self.browser = pw.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.db = SessionLocal()
        self.created_count = 0
        self.updated_count = 0
        self.skipped_count = 0

    def scrape(self):
        try:
            self.page.goto(f"{self.BASE_URL}{self.CAR_LIST_URL}")
            self.__reject_cookies()
            self.__show_more_cars()

            content = self.page.content()
            links = re.findall("<a class=\"link stretched-link\" href=\"(.*)\">", content)

            print(f"\n🚗 Found {len(links)} cars to scrape...")

            for idx, link in enumerate(links, 1):
                print(f"\nProcessing car {idx}/{len(links)}...")
                self.__go_to_car_page(link)

            print("\n" + "=" * 50)
            print("Scraping Summary")
            print("=" * 50)
            print(f"✓ Cars created: {self.created_count}")
            print(f"🔄 Cars updated: {self.updated_count}")
            print(f"⊘ Cars skipped: {self.skipped_count}")
            print(f"Total processed: {len(links)}")
            print("=" * 50)

        finally:
            self.browser.close()
            self.db.close()

    def __show_more_cars(self):
        if self.page.locator("#show-more-cars").is_visible(timeout=3000):
            print('show more cars is visible')
            self.page.locator("#show-more-cars").click()
            print('clicked show more cars')
            time.sleep(1)
            self.__show_more_cars()
        else:
            return

    def __reject_cookies(self):
        self.page.locator("#onetrust-reject-all-handler").click()

    def __go_to_car_page(self, link):
        car_url = f"{self.BASE_URL}/{link}"

        if self.SKIP_EXISTING_CARS and self.db.query(Car).where(Car.external_link == car_url).first():
            print(f"  ⊘ Skipped: {link} - already exists")
            self.skipped_count += 1
            return

        self.page.goto(car_url)

        is_sold = self.page.locator('.product-details-section-col .product-availability-status').inner_text() == 'Såld'

        if is_sold:
            print(f"  ⊘ Skipped: {link} - already sold")
            self.skipped_count += 1
            return

        # Extract car details
        name = self.page.locator('.product-details-section-col .product-name').inner_text()
        description = self.page.locator('.product-details-section-col .product-description').inner_text()
        price_str = self.page.locator('.product-details-section-col .sales .value').get_attribute('content')
        registered_date = self.page.locator('#vehicle-details .registrationDate .value').inner_text()
        fuel_type = self.page.locator('#vehicle-details .fuelType .value').inner_text().lower()
        mileage_str = self.page.locator('#vehicle-details .mileage .value').inner_text()
        color = self.page.locator('#vehicle-details .refinementColor .value').inner_text().lower()
        license_plate = self.page.locator('#vehicle-details .licensePlate .value').inner_text().upper()
        wheel_drive = self.page.locator('#vehicle-details .wheelDrive .value').inner_text().lower()
        make = self.page.locator('.product-breadcrumb').first.locator('.breadcrumb-item:nth-child(2) a').inner_text().replace('\n', '').strip().lower()
        model = self.page.locator('.product-breadcrumb').first.locator('.breadcrumb-item:nth-child(3) span').inner_text().replace('\n', '').strip().lower()

        # Extract image URL if available
        display_image_url = None
        try:
            image_element = self.page.locator('.primary-images .carousel-item.active img').first
            if image_element.is_visible(timeout=2000):
                display_image_url = image_element.get_attribute('src')
        except Exception:
            pass  # Image not found, leave as None

        # Parse and extract data
        year = self.__extract_year(registered_date)
        price = Decimal(price_str) if price_str else None
        mileage = self.__parse_mileage(mileage_str)

        # Check if car already exists by registration number
        existing_car = self.db.query(Car).filter(Car.registration_number == license_plate).first()

        if existing_car:
            # Update existing car with latest data
            existing_car.name = name
            existing_car.brand = self.__to_english(make)
            existing_car.model = self.__to_english(model)
            existing_car.make = make
            existing_car.fuel_type = self.__to_english(fuel_type)
            existing_car.color = self.__to_english(color)
            existing_car.year = year or 2024
            existing_car.price = price
            existing_car.registered_date = registered_date
            existing_car.registered_year = year
            existing_car.mileage = mileage
            existing_car.wheel_drive = self.__to_english(wheel_drive)
            existing_car.variant = description
            existing_car.source = "ayvens"
            existing_car.external_link = car_url
            existing_car.display_image_url = display_image_url

            self.db.commit()
            self.db.refresh(existing_car)

            print(f"  🔄 Updated: {name} ({license_plate})")
            self.updated_count += 1
        else:
            # Create new car in database
            car = Car(
                name=name,
                brand=self.__to_english(make),
                model=self.__to_english(model),
                make=make,  # Using brand as make
                fuel_type=self.__to_english(fuel_type),
                color=self.__to_english(color),
                year=year or 2024,  # Default to current year if not found
                price=price,
                registered_date=registered_date,
                registered_year=year,
                mileage=mileage,
                wheel_drive=self.__to_english(wheel_drive),
                registration_number=license_plate,
                variant=description,
                source="ayvens",
                external_link=car_url,
                display_image_url=display_image_url
            )

            self.db.add(car)
            self.db.commit()
            self.db.refresh(car)

            print(f"  ✓ Created: {name} ({license_plate})")
            self.created_count += 1

    def __extract_year(self, date_string):
        """Extract year from date string."""
        # Try to find a 4-digit year in the string
        match = re.search(r'\b(20\d{2})\b', date_string)
        if match:
            return int(match.group(1))
        return None

    def __parse_mileage(self, mileage_str):
        """Parse mileage string to integer."""
        # Remove non-digit characters except for separators
        cleaned = re.sub(r'[^\d]', '', mileage_str)
        try:
            return int(cleaned) if cleaned else None
        except ValueError:
            return None

    def __to_english(self, text):
        mapping = {
            'elektrisk': 'electric',
            'diesel': 'diesel',
            'bensin': 'petrol',
            'hybrid': 'hybrid',
            'petrol': 'petrol',
            'bensin': 'bensin',
            'vit': 'white',
            'svart': 'black',
            'grå': 'grey',
            'röd': 'red',
            'blå': 'blue',
            'gul': 'yellow',
            'grön': 'green',
            'brun': 'brown',
            'orange': 'orange',
            'bakhjulsdrift': 'rear wheel drive',
        }

        return mapping.get(text, text)


if __name__ == "__main__":
    scraper = AyvensScraper()
    scraper.scrape()
