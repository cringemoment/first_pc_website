import os
from bs4 import BeautifulSoup

def convert_to_relative_links(html_folder):
    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            filepath = os.path.join(html_folder, filename)
            with open(filepath, "r") as file:
                content = file.read()

            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all("a")

            for linkindex, link in enumerate(links):
                href = link.get("href")
                relative_path = os.path.relpath(href, start=html_folder)
                links[linkindex]["href"] = '/'.join(href.split("/")[-2:])

            with open(filepath, "w") as file:
                file.write(soup.prettify())

# Replace 'your_html_folder_path' with the path to your folder containing HTML files
html_folder_path = r"C:\Users\huy cao\Documents\Python Files\first pc website\setups/"
convert_to_relative_links(html_folder_path)
