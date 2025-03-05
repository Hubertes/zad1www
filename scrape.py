import requests
from bs4 import BeautifulSoup
import time

from duckduckgo_search import DDGS

def search_with_retry(query, max_retries=4, retry_delay=30):
    print(f"Searching for {query}")
    for attempt in range(max_retries):
        try:
            results = DDGS().text(query, max_results=5)
            return results
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    print("All attempts failed. Giving up.")
    return None

r = requests.get('https://www.tiobe.com/tiobe-index/')

print("Got status code:", r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')

tables = soup("table")
print("Found", len(tables), "table(s)")

tbody = tables[0].find("tbody")
rows = tbody("tr")

f = open("index.md", "w")

f.write("# Top 20 programming languages:\n")
for row in rows:
    cells = row("td")

    icon = cells[3].find("img")
    filename = cells[4].text.replace("/", "").replace(" ", "-") + ".md"

    f.write("## " + "![](" + "https://www.tiobe.com/" + icon["src"] + ") " + "[" + cells[4].text + "](" + filename + ")\n")
    f.write("- Position last year: " + cells[0].text + "\n")
    f.write("- Position this year: " + cells[1].text + "\n")
    f.write("- Ratings: " + cells[5].text + "\n")
    f.write("- Change in ratings: " + cells[6].text + "\n")

    sf = open(filename, "w")
    sf.write("# " + cells[4].text + "\n")
    search_results = search_with_retry(cells[4].text + " programming language")
    for result in search_results:
        sf.write("## " + result["title"] + " from " + result["href"] + "\n")
        sf.write(result["body"] + "\n")
    sf.close()

f.close()
