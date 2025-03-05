import requests
from bs4 import BeautifulSoup

from duckduckgo_search import DDGS

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
    filename = cells[4].text.replace("/", "") + ".md"

    f.write("## " + "![](" + "https://www.tiobe.com/" + icon["src"] + ") " + "[" + filename + "](" + cells[4].text + ")\n")
    f.write("- Position last year: " + cells[0].text + "\n")
    f.write("- Position this year: " + cells[1].text + "\n")
    f.write("- Ratings: " + cells[5].text + "\n")
    f.write("- Change in ratings: " + cells[6].text + "\n")

    sf = open(filename, "w")
    sf.write("# " + cells[4].text + "\n")
    for result in DDGS().text(cells[4].text + " programming language", max_results=5):
        sf.write("## " + result["title"] + " from " + result["href"] + "\n")
        sf.write(result["body"] + "\n")
    sf.close()

f.close()