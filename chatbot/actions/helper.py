from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, Restarted, AllSlotsReset, UserUtteranceReverted, ActionReverted
import random

module_slots = {
    "moduleTitle": "Module Title",
    "program": "Program",
    "degree": "Degree",
    "courseRegulation": "A Course Regulation",
    "person": "Name of a Responsible Person",
    "ects": "ECTS"
}

mensa_slots = {
    "mensaName": "Mensa Name",
    "menuCourse": "a Course",
    "vegetarian": "Only vegetarian food",
    "vegan": "Only vegan food",
    "price": "A Price",
}


class ActionFallback(Action):
    def name(self):
        return "action_fallback"

    def run(self, dispatcher, tracker, domain):
        did_not_understand = [
            "Sorry I didn't get that.",
            "Try again",
            "What do you mean? (in the voice of Justin Bieber)",
            "I cannot help you with that",
            "I did not understand"
        ]
        dispatcher.utter_message(random.choice(did_not_understand))
        return [UserUtteranceReverted()]


class ActionResetDialogue(Action):
    def name(self):
        return "action_reset_dialogue"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Im resetting our dialogue. Go ahead and start a new one :)")
        return [AllSlotsReset()]


class ActionSetContextModule(Action):
    def name(self):
        return "action_set_context_module"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("You're looking for information related to modules. Would you give me some "
                                 "more information on what you are looking for?")


        return[
            SlotSet("mensaName", None),
            SlotSet("menuCourse", None),
            SlotSet("price", 0.0),
            SlotSet("vegetarian", False),
            SlotSet("vegan", False),
            SlotSet("mensaMatch", None)
        ]


class ActionSetContextMensa(Action):
    def name(self):
        return "action_set_context_mensa"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("You're looking for information related to mensa. Would you give me some more "
                                 "information on what you are looking for?")

        return[
            SlotSet("moduleTitle", None),
            SlotSet("program", None),
            SlotSet("ects", 0.0),
            SlotSet("person", None),
            SlotSet("courseRegulation", None),
            SlotSet("degree", None),
            SlotSet("moduleTitleMatch", None),
            SlotSet("moduleTitleExactMatch", False),
            SlotSet("programExactMatch", False),
            SlotSet("programMatch", None),
            SlotSet("personQuery", None),
            SlotSet("personMatch", None),
            SlotSet("personModuleMatch", None),
            SlotSet("ectsMatch", None)
        ]