import json
import os
import re
import time
from tqdm import tqdm
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Replace with your login credentials
credentials = {
    'username': 'mail@mail.com',  # Replace with your email
    'password': 'password'  # Replace with your password
}

# Path to store the context state (session cookies, etc.)
context_storage_path = './context_state.json'


def login(page):
    """
    Logs in to the website using the provided credentials.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the page does not load as expected.
    """
    try:
        # Fill out the login form
        page.fill("#email", credentials['username'])
        page.fill("#password", credentials['password'])

        # Click the 'Sign in' button
        page.click('button[type="submit"]')

        # Wait for navigation after login
        page.wait_for_load_state("networkidle")
        print("Login completed.")
    except PlaywrightTimeoutError as e:
        print(f"Login failed due to timeout: {e}")
        raise


def click_launch_challenge(page):
    """
    Clicks on the 'Launch Challenge' button after waiting for necessary elements.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the button is not found or the page doesn't load as expected.
    """
    try:
        # Wait for the 'Launch Challenge' button to be visible
        page.wait_for_selector('button:has(svg.lucide-x)', timeout=5000)

        # Click the button that contains the 'lucide-x' SVG
        page.click('button:has(svg.lucide-x)')

        print("Close button clicked.")
        page.wait_for_selector('body')

        page.wait_for_selector('button:has-text("Launch Challenge")')

        # Click on the 'Launch Challenge' button
        page.click('button:has-text("Launch Challenge")')

        # Wait for the next page or relevant content to load after clicking
        page.wait_for_selector("body")  # You can adjust this based on the page load indicator
        print("Launched the challenge.")
    except PlaywrightTimeoutError as e:
        print(f"Failed to click on Launch Challenge: {e}")
        raise


def navigate_to_inventory(page):
    """
    Navigates through the necessary pages to reach the 'Inventory' section.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the page does not load or required buttons are not found.
    """
    try:
        # Wait for the 'Start Journey' button to be visible and click it
        page.wait_for_selector('button:has-text("Start Journey")', timeout=5000)
        page.click('button:has-text("Start Journey")')
        print("Start Journey button clicked.")
        page.wait_for_selector('body')  # Wait for the page or relevant content to load after clicking

        # Wait for the 'Continue Search' button to be visible and click it
        page.wait_for_selector('button:has-text("Continue Search")', timeout=5000)
        page.click('button:has-text("Continue Search")')
        print("Continue Search button clicked.")
        page.wait_for_selector('body')  # Wait for the page or relevant content to load after clicking

        # Wait for the 'Inventory Section' button with the lucide-database icon to be visible and click it
        page.wait_for_selector('button:has(svg.lucide-database)', timeout=5000)
        page.click('button:has(svg.lucide-database)')
        print("Inventory Section button clicked.")
        page.wait_for_selector('body')  # Wait for the page or relevant content to load after clicking
    except PlaywrightTimeoutError as e:
        print(f"Navigation failed: {e}")
        raise


def extract_product_data(page):
    """
    Extracts product details from the page with a progress bar.

    Args:
        page: The Playwright page object representing the browser page.

    Returns:
        A list of dictionaries containing product information.

    Raises:
        Exception: If there is an error while extracting product data.
    """
    try:
        # Selector for the product items
        product_selector = "div.flex.flex-col.sm\\:flex-row.sm\\:items-center.justify-between.p-4.border.rounded-md.hover\\:bg-muted\\/30.transition-colors.animate-fade-in"

        # Extract all product elements
        products = page.query_selector_all(product_selector)

        product_data = []

        # Initialize the progress bar
        for product in tqdm(products, desc="Extracting Products", unit="product"):
            try:
                # Extract product details
                title = product.query_selector("h3.font-medium").inner_text()
                id_ = product.query_selector("span.font-mono").inner_text().split(": ")[1]

                # Extract category from the third span in the flex container
                category = product.query_selector(
                    "div.flex.items-center.text-sm.text-muted-foreground span:nth-child(3)").inner_text()

                composition = product.query_selector(
                    "div.flex.flex-wrap.gap-4.text-sm div:nth-child(1) span.font-medium").inner_text()
                details = product.query_selector(
                    "div.flex.flex-wrap.gap-4.text-sm div:nth-child(2) span.font-medium").inner_text()
                cost = product.query_selector(
                    "div.flex.flex-wrap.gap-4.text-sm div:nth-child(3) span.font-medium").inner_text()
                updated = product.query_selector(
                    "div.flex.flex-wrap.gap-4.text-sm div:nth-child(4) span.font-medium").inner_text()

                # Append the extracted data to the list
                product_data.append({
                    "id": id_,
                    "title": title,
                    "category": category,
                    "composition": composition,
                    "details": details,
                    "cost": cost,
                    "updated": updated
                })
            except Exception as e:
                print(f"Error extracting data from a product: {e}")

        return product_data
    except Exception as e:
        print(f"Error while extracting product data: {e}")
        raise


def scroll_page_until_end(page):
    """
    Scrolls the page until all products are loaded or a limit is reached.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        PlaywrightTimeoutError: If the page does not load or the scrolling does not work as expected.
    """
    prev_height = -1
    max_scrolls = 100
    scroll_count = 0

    try:
        while scroll_count < max_scrolls:
            # Scroll to the bottom using JavaScript
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)  # Wait for content to load

            # Check if scroll height has changed
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                break

            # Extract the number of products shown and total products from the HTML
            products_info = page.query_selector("div.flex.justify-between.items-center.px-2")
            if products_info:
                products_text = products_info.inner_text()

                # Use regular expressions to extract numbers
                match = re.search(r"Showing (\d+) of (\d+) products", products_text)
                if match:
                    shown_products = int(match.group(1))  # First number (shown products)
                    total_products = 100  # Second number (total products)

                    print(f"Shown Products: {shown_products}, Total Products: {total_products}")

                    # Stop scrolling if all products are shown
                    if shown_products >= total_products:
                        print("All products are displayed.")
                        return

            prev_height = new_height
            scroll_count += 1
    except PlaywrightTimeoutError as e:
        print(f"Scrolling failed: {e}")
        raise


def save_to_json(data):
    """
    Saves the extracted product data to a JSON file.

    Args:
        data: The data to be saved, in the form of a list of dictionaries.
    """
    output_path = "productData.json"
    try:
        with open(output_path, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {output_path}.")
    except IOError as e:
        print(f"Error saving data to JSON: {e}")


def start_browser():
    """
    Starts the browser, performs login, navigates to the challenge, extracts data,
    and saves it to a JSON file.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            # Create a new context and page
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://hiring.idenhq.com/")

            # Check if the user is already logged in by looking for the login button
            login_button = page.query_selector('button[type="submit"]')

            if login_button:
                print("User is not logged in, proceeding with login...")
                login(page)  # Proceed with login
            else:
                print("User is already logged in, skipping login...")

            # Wait for the page to load and click the 'Launch Challenge' button
            click_launch_challenge(page)
            navigate_to_inventory(page)

            # Extract product data
            scroll_page_until_end(page)
            print("Extracting Data")
            product_data = extract_product_data(page)
            print(product_data)

            # Save the extracted data to a JSON file
            save_to_json(product_data)

            # Close the browser
            browser.close()
            # Keep the browser open for a while
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    start_browser()
