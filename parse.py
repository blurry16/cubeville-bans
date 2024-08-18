import json
import logging
from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup
from requests import get

logging.basicConfig(level=logging.INFO)

BANS_URL = "https://www.cubeville.org/cv-site/banlist.php"


class JsonFile:
    """JsonFile class contains required methods to work with .json files"""

    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = Path(file_path)

    def load(self) -> dict | list:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, data: dict | list, indent: int = 2) -> None:
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            json.dump(data, data_file, indent=indent)


logging.info("Parsing HTML...")
soup = BeautifulSoup(get(BANS_URL).content, "html.parser")
logging.info("Successfully parsed HTML.")
# html = soup.prettify()
main_content = str(soup.find_all(id="main-content")[1])

datafile = JsonFile("bans.json")

rows = "\n".join(main_content.split("</tr>")).split("<tr>")
pprint(rows)
logging.info("Successfully formatted the rows")

placeholder = "<github.com/blurry16>"
string = "\n".join(placeholder.join("".join("".join(rows).split("<td>")[1:]).split("</td>")).split("\n")[:-3]).replace(
    "\r\n", "")  # dont ask me what in the name of freak is this.  ~ It just works ~.
pprint(string)
logging.info("Successfully formatted the string.")
with open("data", "w") as file:
    file.write(string)

data = []
for i in reversed(string.split("\n")):
    split = i.split(placeholder)[:-1]  # except for the last one cus the last one is an empty string
    print(split)
    try:
        data.append({
            "name": split[0],
            "date": split[1],
            "reason": split[2],
            "duration": split[3],
        })
    except IndexError as error:
        logging.error(error)
datafile.dump(data)
logging.info("Successfully dumped data into the file.")
print(f"\n{len(datafile.load())} players banned in total. :P")
