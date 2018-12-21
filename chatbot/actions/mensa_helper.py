from datetime import datetime

from mensa.mensa_requests import *
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, UserUtteranceReverted, ActionReverted


mensa_data_cache: dict = {}
mensa_menu_cache: dict = {}


class ActionCheckMensaNames(Action):
    def name(self):
        return "action_check_mensa_names"

    def run(self, dispatcher, tracker, domain):
        mensa_name_list_slots: list = tracker.get_slot("mensaName")
        mensa_name_list: list = []
        mensa_match_amount = 0
        for mensa_name in mensa_name_list_slots:
            mensa_id = get_mensa_id(mensa_name)
            if mensa_id:
                mensa_match_amount += 1
                mensa_name_list.append(mensa_name)

        # HINT: think about this behaviour
        if mensa_match_amount == 0:
            mensa_match = "zero"
            dispatcher.utter_message("Sorry I couldn't extract any mensa names from your message, please try again.")
            return [SlotSet("mensaMatch", mensa_match),
                    SlotSet("mensaName", None)]

        elif mensa_match_amount == 1:
            mensa_match = "one"
        else:
            mensa_match = "multiple"

        return [SlotSet("mensaMatch", mensa_match), SlotSet("mensaName", mensa_name_list)]


class ActionCheckPrice(Action):
    def name(self):
        return "action_check_price"

    def run(self, dispatcher, tracker, domain):
        price = tracker.get_slot("price")
        if type(price) != float:
            try:
                price = float(str(price).replace(",", ".").replace(" ", ""))
            except ValueError:
                dispatcher.utter_message("Sorry I couldn't identify your input as a price value. "
                                         "I will reset your input, please try again.")
                return [SlotSet("price", 0.0), UserUtteranceReverted(), ActionReverted()]

        return [SlotSet("price", price)]


class ActionCheckMenuCourse(Action):
    possible_courses = {
        **dict.fromkeys(["suppen", "suppe", "soup"], "Suppen"),
        **dict.fromkeys(["aktionen", "aktion", "special offer"], "Aktionen"),
        **dict.fromkeys(["beilagen", "beilage", "side dish", "side dishes"], "Beilagen"),
        **dict.fromkeys(["dessert", "dessert", "nachtisch"], "Desserts"),
        **dict.fromkeys(["essen", "food", "main dish"], "Essen"),
        **dict.fromkeys(["vorspeisen", "vorspeise", "starters"], "Vorspeisen"),
        **dict.fromkeys(["salate", "salat", "salad", "salads"], "Salate"),
    }

    def name(self):
        return "action_check_menu_course"

    def run(self, dispatcher, tracker, domain):
        menu_courses: list = tracker.get_slot("menuCourse")
        if type(menu_courses) != list:
            dispatcher.utter_message("Sorry I couldn't extract a Course for your menu search, "
                                     "I will reset this information")
            return [SlotSet("menuCourse", None), UserUtteranceReverted(), ActionReverted()]

        new_menu_courses = []
        for menu_course in menu_courses:
            menu_course_formatted = menu_course.lower()
            if menu_course_formatted in self.possible_courses:
                new_menu_courses.append(self.possible_courses[menu_course_formatted])

        if len(new_menu_courses) == 0:
            dispatcher.utter_message("Sorry I couldn't extract a Course for your menu search, "
                                     "I will reset this information")
            return [SlotSet("menuCourse", None), UserUtteranceReverted(), ActionReverted()]
        else:
            dispatcher.utter_message("I extracted the following Courses from your input:")
            dispatcher.utter_message(", ".join(new_menu_courses))
            return [SlotSet("menuCourse", new_menu_courses)]


class ActionSetVegetarianTrue(Action):
    def name(self):
        return "action_set_vegetarian_true"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("vegetarian", True)]


class ActionSetVeganTrue(Action):
    def name(self):
        return "action_set_vegan_true"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("vegan", True)]


class ActionResetFoodRestrictions(Action):
    def name(self):
        return "action_reset_food_restrictions"

    def run(self, dispatcher, tracker, domain):

        return [SlotSet("vegan", False), SlotSet("vegetarian", False)]


# HINT: keep this updated with all mensa related slots
mensa_slots = {
    "mensaName": "Mensa Name",
    "menuCourse": "a Course",
    "vegetarian": "Only vegetarian food",
    "vegan": "Only vegan food",
    "price": "A Price",
}


class ActionAskForMoreMensaInformation(Action):
    def name(self):
        return "action_ask_for_more_mensa_information"

    @staticmethod
    def create_message_for_available_information(available_information):
        message = "Here is information I already extracted from our conversation:\n"
        for slot in available_information:
            if type(slot[1]) == list:
                if slot[0] == "mensaName":
                    mensa_names = [get_mensa_name(get_mensa_id(mensa_name)) for mensa_name in slot[1]]
                    message += mensa_slots[slot[0]] + ": " + ", ".join(mensa_names) + "\n"
                elif slot[0] == "menuCourse":
                    message += mensa_slots[slot[0]] + ": " + ", ".join(slot[1]) + "\n"
            elif type(slot[1]) == bool:
                message += str(mensa_slots[slot[0]]) + ": " + ("yes" if slot[1] else "no") + "\n"
            else:
                if slot[0] == "price":
                    message += str(mensa_slots[slot[0]]) + ": " + str("%.2f" % slot[1]) + " €\n"
                else:
                    message += str(mensa_slots[slot[0]]) + ": " + str(slot[1]) + " €\n"

        return message

    @staticmethod
    def create_message_for_possible_information(possible_information):
        message = "Here are some more things you could specify: "
        message += ', '.join(map(lambda slot: mensa_slots[slot], possible_information))
        return message

    def run(self, dispatcher, tracker, domain):
        available_information = []  # slots that are already filled (should be checked)
        possible_information = []  # slots that could be filled
        for mensa_slot in mensa_slots:
            slot_entry = tracker.get_slot(mensa_slot)
            if slot_entry:
                if mensa_slot == "price":
                    if slot_entry == 0.0 and type(slot_entry) != float:
                        possible_information.append(mensa_slot)
                    else:
                        available_information.append((mensa_slot, slot_entry))
                elif mensa_slot in ("vegetarian", "vegan"):
                    if not slot_entry:
                        possible_information.append(mensa_slot)
                    else:
                        available_information.append((mensa_slot, slot_entry))
                else:
                    available_information.append((mensa_slot, slot_entry))
            else:
                possible_information.append(mensa_slot)

        message = ""
        if len(available_information) > 0:
            message += self.create_message_for_available_information(available_information)
        if len(possible_information) > 0:
            message += self.create_message_for_possible_information(possible_information)

        dispatcher.utter_message(message)
        dispatcher.utter_message("You can also tell me to show you menus or information about mensas."
                                 " And I will try to look for something using the clues you gave me so far.")
        return []


class ActionShowMensaData(Action):
    def name(self):
        return "action_show_mensa_data"

    @staticmethod
    def date2string(dates):
        date_string = ""
        for date in dates:
            opening_hours_date: datetime.datetime = date[0][0]
            closing_hours_date: datetime.datetime = date[1][0]
            day = opening_hours_date.strftime("%A")
            opening_time = opening_hours_date.strftime("%H:%M")
            closing_time = closing_hours_date.strftime("%H:%M")
            date_string += "{:10} {:>12}\n".format(day, (opening_time + "-" + closing_time))
        return date_string

    def create_message(self, mensa):
        message = "Name: " + str(mensa["name"]) + "\nWebsite: " + str(mensa["website"]) \
                  + "\nPhone: " + str(mensa["phone"]) + \
                  "\nAddress:\n" + str(mensa["address"]) + "\n"
        date = "Opening Hours:\n" + self.date2string(mensa["opening_hours"])
        message += date
        return message

    def run(self, dispatcher, tracker, domain):
        mensa_name_list: list = tracker.get_slot("mensaName")

        if not mensa_name_list:
            mensa_name_list = id2mensa
            dispatcher.utter_message("Here's information for all mensas")
        else:
            dispatcher.utter_message("Here's the information I found for your specified mensas")

        for mensa_name in mensa_name_list:
            mensa_id = get_mensa_id(mensa_name)
            if mensa_id not in mensa_data_cache:
                mensa = MensaRequest(mensa_name).get_mensa_data()
                print(mensa)
                if mensa:
                    mensa_data_cache[mensa[0]] = mensa[1]

            message = self.create_message(mensa_data_cache[mensa_id])
            dispatcher.utter_message(message)
        dispatcher.utter_message("Can I help you with anything else?")
        return []


class ActionShowMensaFood(Action):
    def name(self):
        return "action_show_mensa_menu"

    @staticmethod
    def create_message(mensa_menu, vegetarian=False, vegan=False, price=0.0, menu_courses=None):
        if not mensa_menu:
            return "Closed or not serving food today."
        message = ""
        for menu_item in mensa_menu:

            if vegetarian:
                if not menu_item["vegetarian"]:
                    continue
            if vegan:
                if not menu_item["vegan"]:
                    continue

            if price and price > 0.0:
                if not menu_item["price_student"] <= price:
                    continue

            if menu_courses:
                if menu_item["course"] not in menu_courses:
                    continue
            # HINT: only showing and handling student price
            if not menu_item["price_student"]:
                message += (menu_item["name"] + " price: " + "Not specified\n")
            else:
                message += (menu_item["name"] + " price: " + str("%.2f" % float(menu_item["price_student"])) + "€\n")

        if len(message) == 0:
            message = "Couldn't find anything for your restrictions."
        return message

    def run(self, dispatcher, tracker, domain):
        mensa_name_list: list = tracker.get_slot("mensaName")
        vegetarian: bool = tracker.get_slot("vegetarian")
        vegan: bool = tracker.get_slot("vegan")
        price: float = tracker.get_slot("price")
        menu_courses = tracker.get_slot("menuCourse")

        dispatcher.utter_message("Here are the menus I found for your specified mensas:")
        # if mensa_name_list not set iterate over all mensas
        for mensa_name in (id2mensa if not mensa_name_list else mensa_name_list):
            mensa_id = get_mensa_id(mensa_name)

            # Hint: just handling today for now if weekend choose next monday
            date = datetime.datetime.today()
            if date.weekday() in (5, 6):
                date = (date + datetime.timedelta((0 - date.weekday()) % 7))

            date_str = date.strftime("%Y-%m-%d")

            if (mensa_id, date_str) not in mensa_menu_cache:
                mensa_menu = MensaRequest(mensa_name, date).get_mensa_menu()
                mensa_menu_cache[(mensa_menu[0], mensa_menu[1].strftime("%Y-%m-%d"))] = mensa_menu[2]

            message = "Here is the food I found using your restrictions for the " + str(
                get_mensa_name(mensa_id)) + " on the " + date_str + ":\n"
            message += self.create_message(mensa_menu_cache[(mensa_id, date_str)], vegetarian,
                                           vegan, price, menu_courses)
            dispatcher.utter_message(message)
        dispatcher.utter_message("Can I help you with anything else?")
        return []
