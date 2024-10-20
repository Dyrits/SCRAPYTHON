from pprint import pprint
import requests
from bs4 import BeautifulSoup

def fetch(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.HTTPError as exception:
        print("[Error] HTTP: ", exception)
    except requests.exceptions.ConnectionError as exception:
        print("[Error] Connection: ", exception)
    except requests.exceptions.Timeout as exception:
        print("[Error] Timeout: ", exception)
    except requests.exceptions.RequestException as exception:
        print("[Error] Request: ", exception)

def write(filename: str, data: str) -> None:
    with open(filename,"w",encoding = "utf-8") as file:
        file.write(data)

def traverse(element, level = 0):
    print(f"{'  ' * level} {element.name} {element.attrs}")
    for child in element.children:
        if child.name:
            traverse(child, level + 1)

try :
    html = fetch("https://books.toscrape.com/") # Fetch the data from the URL.
    write("index.html", html) # Write the fetched data to a file.
    soup = BeautifulSoup(html, "html.parser") # Parse the fetched data using BeautifulSoup.
    # print(soup.prettify()) # Print the parsed data in a readable format.
    # traverse(soup) # Traverse the parsed data.
    division = soup.find("div", class_="side_categories") # Find the div tag with the class name "side_categories".
    categories = division.ul.li.ul.find_all("a") # Find all the anchor tags in the division.
    for category in categories:
        text = category.get_text(strip = True) # Get the text of the anchor tag.
        print(text) # Print the text of the anchor tag.
    images = soup.find_all("img", alt=True) # Find all the image tags with the alt attribute.
    for image in images:
        src = image.get("src") # Get the source of the image.
        alt = image.get("alt") # Get the alt text of the image.
        print(f"Source: {src} | Alt: {alt}") # Print the source and alt text of the image.
    articles = soup.find_all("article", class_="product_pod") # Find all the article tags with the class name "product_pod".
    for article in articles:
        title = article.h3.a.get("title") # Get the title of the article.
        price = article.find("p", class_="price_color").get_text() # Get the price of the article.
        print(f"Title: {title} | Price: {price}")
except Exception as exception:
    print("[Error] ", exception)