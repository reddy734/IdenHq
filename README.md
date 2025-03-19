# Playwright Web Scraper

## Overview
This Python project automates the process of logging into the `https://hiring.idenhq.com/` website, navigating through various pages, extracting product details, and saving them into a JSON file. It uses [Playwright](https://playwright.dev/python/) for browser automation and [tqdm](https://pypi.org/project/tqdm/) for progress visualization.

## Features
- **Automated Login**: Logs in with provided credentials.
- **Navigation**: Clicks through the necessary buttons to access the inventory.
- **Product Data Extraction**: Scrapes product details like title, category, cost, and updated information.
- **Infinite Scrolling**: Scrolls until all products are loaded.
- **JSON Output**: Saves extracted data into a structured JSON file.
- **Error Handling**: Handles timeouts and missing elements gracefully.

## Prerequisites
Ensure you have the following installed:
- Python 3.7+
- Playwright
- tqdm

## Installation
Clone this repository:
```sh
git clone https://github.com/your-username/playwright-web-scraper.git
cd playwright-web-scraper
```

Install dependencies:
```sh
pip install -r requirements.txt
```

Set up Playwright browsers:
```sh
playwright install
```

## Configuration
Update the `credentials` dictionary in `main.py` with your login credentials:
```python
credentials = {
    'username': 'your-email@example.com',
    'password': 'your-password'
}
```

## Usage
Run the script:
```sh
python main.py
```
This will:
1. Open the website.
2. Log in (if not already logged in).
3. Click through required buttons.
4. Extract and save product data to `productData.json`.

## Output
The extracted data is saved in `productData.json` in the following format:
```json
[
  {
    "id": "12345",
    "title": "Product Name",
    "category": "Electronics",
    "composition": "Plastic & Metal",
    "details": "Some details",
    "cost": "$100",
    "updated": "2025-03-19"
  }
]
```

## Troubleshooting
- If login fails, ensure the credentials are correct.
- If Playwright isn't installed, run `playwright install`.
- If the script fails to find elements, check the website for UI changes and update selectors.

## License
This project is licensed under the MIT License.

## Contributing
Feel free to fork and submit pull requests for improvements!

---

Happy Scraping! 🚀

