from typing import Dict, List, Any, Union, Tuple

import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
from dateutil.rrule import rrule, WEEKLY
import logging

BASE_URL_DATA = "https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html"
BASE_URL_MENU = "https://www.stw.berlin/xhr/speiseplan-wochentag.html"

mensa2id = {
    **dict.fromkeys(["hardenberg", "haupt", "hauptmensa", "hardenbergmensa", "321"], "321"),
    **dict.fromkeys(["skyline cafe", "skyline", "cafe skyline" "tel", "657"], "657"),
    **dict.fromkeys(["march", "mar", "marmensa", "marchgebäude", "mar cafe", "march cafeteria", "538"], "538"),
    **dict.fromkeys(["wetterleuchte", "wetterleuchten", "hauptgebaudecafe", "cafe wetterleuchte",
                    "wetterleuchten cafe", "541"], "541"),
    # TODO: add more cafeterias
}

id2mensa = {
    "321": "Hardenbergmensa",
    "657": "Skyline Café",
    "538": "March Cafeteria",
    "541": "Wetterleuchten Café"
}


def get_mensa_id(mensa):
    # get's a raw mensa-name transforms this to lowercase and replaces unicode characters with
    # normal ascii characters (ä -> a) and if that name exist the corresponding id is returned
    return mensa2id.get(unidecode.unidecode(mensa.lower()))


def get_mensa_name(mensa_id):
    # defines the name for mensas
    return id2mensa.get(mensa_id)


class MensaRequest:

    weekday_translation = {
        "Mo.": 0,
        "Di.": 1,
        "Mi.": 2,
        "Do.": 3,
        "Fr.": 4,
        "Sa.": 5,
        "So.": 6
    }

    def __init__(self, mensa, date=None):
        if not isinstance(mensa, str):
            raise ValueError("mensa  must be from type list and only contain strings")
        if date and not (isinstance(date, datetime.datetime)):
            raise ValueError("date must be of type datetime.datetime or None")
        if not date:
            date = datetime.datetime.now()

        self.mensa = mensa
        self.mensa_id = get_mensa_id(mensa)
        self.date = date

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("chardet.charsetprober").setLevel(logging.DEBUG)

    def _get_page_soup(self, url, date=None):
        # expects a mensa which is contained in the mensa_dict and can handle a date in the format YYYY-MM-DD
        # returns the page content as BeautifulSoup object

        # all the payload for the POST request
        if not self.mensa_id:
            logging.debug("Mensa: " + self.mensa + " not found")
            return None
        data = {"resources_id": self.mensa_id, "date": date}
        headers = {"User-Agent": "Mozilla/5.0"}

        # HTTP request
        page = requests.post(url, data, headers=headers)
        if page.status_code != 200:
            raise ConnectionRefusedError("Couldn't connect to the stw-website ERROR: {}".format(page.status_code))

        # logging.debug(page.content)
        return BeautifulSoup(page.content, "html.parser")

    def get_mensa_menu(self):
        # cf. https://gitlab.tubit.tu-berlin.de/thilo.michael/alex-studiprojekt-ss17/blob/mensa/mensa/mensaCrawler
        # /crawler.py this function requests all dishes available in a specific day for a specific mensa return a
        # list of dictionaries
        # TODO: describe datatype somewhere
        # logging.debug("\nMensa: " + self.mensa + '\n' + "Date: " + str(self.date))
        url = BASE_URL_MENU
        date_for_request = self.date.strftime("%Y-%m-%d")
        page_soup = self._get_page_soup(url, date_for_request)
        if not page_soup:
            return None
        food_offer = unidecode.unidecode(page_soup.find("div", class_="container-fluid splGroupWrapper")
                                         .get_text().strip().lower())
        if food_offer == "kein speisenangebot":
            logging.debug("No food food_offer on: "
                          + self.date.strftime("%d-%m-%Y") + " for Mensa: " + self.mensa_id)
            return self.mensa_id, self.date, None

        # list to be filled in
        food_list = []
        icon_translations = {
            "ampel_gruen_70x65.png": "green",
            "ampel_gelb_70x65.png": "yellow",
            "ampel_rot_70x65.png": "red",
            "1.png": "vegetarian",
            "15.png": "vegan",
            "18.png": "bio",
            "38.png": "marine",
            "43.png": "climate"
        }

        for course in page_soup.findAll("div", class_="container-fluid splGroupWrapper"):
            curr_course = course.find_next("div", class_="col-md-12 splGroup").get_text()
            for dish in course.findAll("div", class_="row splMeal"):
                food_item = _MensaFood()
                # extract course information
                food_item.course = curr_course

                # extract name information
                food_item.name = dish.find_next("span").get_text()

                # extract price information
                # logging.info("Price: " + dish.find_next("div", class_="col-xs-6 col-md-3 text-right")
                # .get_text().strip())
                prices = dish.find_next("div", class_="col-xs-6 col-md-3 text-right").get_text().strip()
                if prices != "":
                    prices = list(map(float, dish.find_next("div", class_="col-xs-6 col-md-3 text-right").get_text()
                                      .split()[1].replace(',', '.').split('/')))
                    if len(prices) == 3:
                        food_item.price_student = prices[0]
                        food_item.price_employee = prices[1]
                        food_item.price_extern = prices[2]
                    else:
                        food_item.price_student = food_item.price_employee = food_item.price_extern = prices[0]

                # extract tag information
                # HINT: this has to be a String because there are tags like "21a"
                food_item.tags = dish.find_next("div", class_="kennz ptr toolt").contents[0] \
                    .strip("\n\r ()").split(", ")

                # extract information based on icons
                for icon in dish.find_next("div", class_="col-xs-12 col-md-3").findAll("img"):
                    icon_src = icon.get("src").split('/')[-1:][0]
                    if "ampel" in icon_src:
                        food_item.traffic_light = icon_translations[icon_src]
                    else:
                        setattr(food_item, icon_translations[icon_src], True)
                food_list.append(food_item.get_mensa_food_dict())

        return self.mensa_id, self.date, food_list

    def get_mensa_data(self) -> (str, dict):
        # {
        # "name": ..,
        # "address": ..,
        # "website": ..,
        # "email": ..,
        # "phone": ..,
        # "opening_hours": ..,
        # "opening_hours_additional": ..,
        # "transfer": ..,
        # }
        url = BASE_URL_DATA
        page_soup = self._get_page_soup(url)
        if not page_soup:
            return None
        # dict to be filled in
        mensa_data: Dict[str, Union[Union[None, str, List[Tuple[List[Any], List[Any]]], List[str]], Any]] = {
            "name": None,
            "address": None,
            "website": None,
            "email": None,
            "phone": None,
            "opening_hours": None,
            "opening_hours_additional": None,
            "transfer": None
        }
        # extracting information
        # HINT: this uses an icon as orientation, which isn't that nice
        # extract name information
        name_information = page_soup.find(selected="selected").get_text()
        mensa_data["name"] = name_information
        # extract address information
        address_elements = page_soup.find(class_="glyphicon glyphicon-map-marker").parent.find_next("div")
        street = address_elements.contents[0].strip()
        postcode = address_elements.contents[4].strip()
        district = address_elements.find_all_next("small")[1].contents[0].strip("()")
        mensa_data["address"] = '\n'.join([street, postcode, district])

        # extract website information
        mensa_data["website"] = page_soup.find(id="directlink").get_text()
        # extract email information
        mensa_data["email"] = page_soup.find(class_="glyphicon glyphicon-envelope").parent.find_next("a").contents[0]

        # extract phone information
        mensa_data["phone"] = page_soup.find(class_="glyphicon glyphicon-earphone") \
            .parent.find_next("div").contents[0].strip()

        # extract opening hours
        def _create_opening_hours_list(hours):
            # function to create a data format, which makes it possible to check
            # if a mensa is open on a specific day/time
            # data format: opening_hours_list = [([opening-datetime-of-weekday-for-next-four-weeks],
            #                                           [closing-datetime-of-weekday-for-next-four-weeks]), ...]
            # TODO: explain/code check_if_open(when<datetime>)
            opening_hours_list = []
            if unidecode.unidecode(hours[1]) == '-':  # handling day interval
                for day in range(self.weekday_translation[hours[0]], self.weekday_translation[hours[2]] + 1):
                    opening_unformatted = hours[3].split(':')
                    opening = list(rrule(dtstart=datetime.datetime.now()
                                         .replace(hour=int(opening_unformatted[0]), minute=int(opening_unformatted[1]),
                                                  second=0), freq=WEEKLY, count=4, byweekday=day))
                    closing_unformatted = hours[5].split(':')
                    closing = list(rrule(dtstart=datetime.datetime.now().
                                         replace(hour=int(closing_unformatted[0]), minute=int(closing_unformatted[1]),
                                                 second=0), freq=WEEKLY, count=4, byweekday=day))
                    opening_hours_list.append((opening, closing))
            else:  # handling a single day
                day = self.weekday_translation[hours[0]]
                opening_unformatted = hours[1].split(':')
                opening = list(rrule(dtstart=datetime.datetime.now()
                                     .replace(hour=int(opening_unformatted[0]), minute=int(opening_unformatted[1]),
                                              second=0), freq=WEEKLY, count=4, byweekday=day))
                closing_unformatted = hours[3].split(':')
                closing = list(rrule(dtstart=datetime.datetime.now().
                                     replace(hour=int(closing_unformatted[0]), minute=int(closing_unformatted[1]),
                                             second=0), freq=WEEKLY, count=4, byweekday=day))
                opening_hours_list.append((opening, closing))
            return opening_hours_list

        opening_hours_information_list = []
        opening_hours_additional_information = []
        curr_div = page_soup.find(class_="glyphicon glyphicon-time").parent.find_next("div")
        while len(curr_div.contents) < 2 or "transfer" not in str(curr_div.contents[1]):
            if len(curr_div.contents) > 4:
                opening_hours_information = curr_div.contents[3]
                if opening_hours_information and not isinstance(opening_hours_information, str):
                    opening_hours_information_formatted = opening_hours_information.get_text().split()
                    if opening_hours_information_formatted[0] in self.weekday_translation.keys():
                        opening_hours_information_list \
                            .extend(_create_opening_hours_list(opening_hours_information_formatted))
                    else:
                        opening_hours_additional_information.append(' '.join(opening_hours_information_formatted))

            curr_div = curr_div.find_next("div")
        mensa_data["opening_hours"] = opening_hours_information_list
        mensa_data["opening_hours_additional"] = opening_hours_additional_information
        # extract transfer information
        transfer_information_list = []
        transfer_elements = page_soup.find(class_="glyphicon glyphicon-transfer").parent.find_next("div").contents
        for element in transfer_elements:
            if isinstance(element, str):
                if element.strip():
                    transfer_information_list.append(element.replace('\xa0', ' '))
            else:
                transfer_information_list.append(element.get_text().strip())
        mensa_data["transfer"] = ''.join(transfer_information_list)
        return self.mensa_id, mensa_data


class _MensaFood:
    name = None
    course = None
    price_student = None
    price_employee = None
    price_extern = None
    tags = None
    traffic_light = None
    vegetarian = None
    vegan = None
    climate = None
    bio = None
    marine = None

    def __init__(self):
        self.vegetarian = False
        self.vegan = False
        self.climate = False
        self.bio = False
        self.marine = False
        return

    def get_mensa_food_dict(self):
        mensa_food_dict = {
            "name": self.name,
            "course": self.course,
            "price_student": self.price_student,
            "price_employee": self.price_employee,
            "price_extern": self.price_extern,
            "tags": self.tags,
            "traffic_light": self.traffic_light,
            "vegetarian": self.vegetarian,
            "vegan": self.vegan,
            "climate": self.climate,
            "bio": self.bio,
            "marine": self.marine
        }
        return mensa_food_dict
