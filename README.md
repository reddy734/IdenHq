# Product Data Scraper

This repository contains a script that automates the process of logging into a website, navigating to a specific challenge, extracting product data, and saving the results to a JSON file using Playwright and Python.

## Prerequisites

To run the code, ensure you have the following installed:

- Python 3.x
- [Playwright](https://playwright.dev/python/docs/intro)
- [tqdm](https://tqdm.github.io/) (for the progress bar)
- [JSON module](https://docs.python.org/3/library/json.html) (standard in Python)

### Install Playwright and required dependencies:

1. Install Playwright:
    ```bash
    pip install playwright
    ```

2. Install the required browsers:
    ```bash
    playwright install
    ```

3. Install other dependencies:
    ```bash
    pip install tqdm
    ```

## Configuration

Before running the script, make sure to set your credentials in the `credentials` dictionary in the script (`main.py`):

```python
credentials = {
    'username': 'your_email@example.com',  # Replace with your email
    'password': 'your_password'  # Replace with your password
}
