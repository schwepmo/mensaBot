from peewee import ModelSelect

from module.models import *
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, Restarted, AllSlotsReset, UserUtteranceReverted, ActionReverted
import itertools


class ActionCheckModuleTitle(Action):
    def name(self):
        return "action_check_module_title"

    def run(self, dispatcher, tracker, domain):
        module_title: str = tracker.get_slot("moduleTitle")

        # HINT: think about this behaviour
        if not module_title:
            dispatcher.utter_message("Sorry I couldn't extract a module title from your message, please try again.")
            return [SlotSet("moduleTitleMatch", "zero"),
                    SlotSet("moduleTitle", None)]

        query = MTSModule.select().where(MTSModule.title ** module_title)
        query_count = query.count()
        if query_count > 0:
            module_title_exact_match = True
        else:
            query = MTSModule.select().where(MTSModule.title.contains(module_title))
            query_count = query.count()
            module_title_exact_match = False

        if query_count == 0:
            module_title_match = "zero"
            dispatcher.utter_message("Sorry I couldn't find any Modules with the name " + module_title + ". " +
                                     "I'm resetting your input.")
            return [SlotSet("moduleTitleMatch", module_title_match),
                    SlotSet("moduleTitle", None)]

        elif query_count == 1:
            module_title_match = "one"
        else:
            module_title_match = "multiple"

        dispatcher.utter_message("I found " + str(query_count) + " modules for the title description " + module_title +
                                 ".")
        if query_count > 0:
            module_list = []
            for module in query:
                module_list.append(module.title)
            message = ", ".join(module_list)
            dispatcher.utter_message(message)

        return [SlotSet("moduleTitleMatch", module_title_match),
                SlotSet("moduleTitleExactMatch", module_title_exact_match)]


class ActionCheckProgram(Action):
    def name(self):
        return "action_check_program"

    def run(self, dispatcher, tracker, domain):
        program: str = tracker.get_slot("program")
        degree: str = tracker.get_slot("degree")
        program_exact_match = False
        if program and degree:
            query = Program.select().where((Program.name.contains(program)) & (Program.degree.contains(degree)))
            message_amount = "using the Program Name: " + program + " and the Degree: " + degree + "."
        elif program:
            query = Program.select().where(Program.name ** program)
            if query.count() > 0:
                program_exact_match = True
            else:
                query = Program.select().where(Program.name.contains(program))
            message_amount = "using the Program Name: " + program + "."
        elif degree:
            query = Program.select().where(Program.degree.contains(degree))
            message_amount = "using the Degree: " + degree + "."
        else:
            # HINT: think about this behaviour
            dispatcher.utter_message("Sorry I couldn't extract a program from your message, please try again.")
            return [SlotSet("programMatch", "zero"),
                    SlotSet("program", None),
                    SlotSet("degree", None)]

        query_count = query.count()
        dispatcher.utter_message("I found " + str(query_count) + " programs " + message_amount)

        if query_count == 0:
            program_match = "zero"
            dispatcher.utter_message("I'm resetting the Program and Degree you gave me,"
                                     " because I can't find a matching Program."
                                     " Feel free to try again.")
            return [SlotSet("programMatch", program_match),
                    SlotSet("program", None),
                    SlotSet("degree", None)]
        elif query_count == 1:
            program_match = "one"
            dispatcher.utter_message(
                "Here is the program I found: " + str(query[0].name) + ", " + str(query[0].degree) + "\n" +
                "You can specify your Course Regulation or just look through all of them."
            )
        else:
            program_match = "multiple"
            message = "Here are the programs I found: \n"
            for found_program in query:
                message += "Name: " + str(found_program.name) + " Degree: " + str(found_program.degree) + "\n"

            dispatcher.utter_message(message)
            if not program:
                dispatcher.utter_message("To thin out the programs I found try to specify a concrete program name.")
            if not degree:
                dispatcher.utter_message("To thin out the programs I found try to specify a degree.")

        return [SlotSet("programMatch", str(program_match)),
                SlotSet("programExactMatch", program_exact_match)]


class ActionCheckCourseRegulations(Action):
    def name(self):
        return "action_check_course_regulations"

    def run(self, dispatcher, tracker, domain):
        program: str = tracker.get_slot("program")
        degree: str = tracker.get_slot("degree")
        course_regulation_slot: str = tracker.get_slot("courseRegulation")

        if program and degree:
            lookup_programs = Program.select().where((Program.name.contains(program)) &
                                                     (Program.degree.contains(degree)))
        elif program:
            lookup_programs = Program.select().where(Program.name.contains(program))
        elif degree:
            lookup_programs = Program.select().where(Program.degree.contains(degree))
        else:
            lookup_programs = None

        if lookup_programs:
            if course_regulation_slot:
                found_course_regulations = (
                    CourseRegulation.select().where((CourseRegulation.program.in_(lookup_programs)))
                )
                course_regulation_constraints = course_regulation_slot.split(" ")
                if len(course_regulation_constraints) == 1:
                    found_course_regulations = (
                        found_course_regulations.where((CourseRegulation.name.contains(course_regulation_slot)) |
                                                       (CourseRegulation.group.contains(course_regulation_slot)))
                                                )
                else:
                    for course_regulation_constraint in course_regulation_constraints:
                        found_course_regulations = (
                            found_course_regulations.where(
                                (CourseRegulation.name.contains(course_regulation_constraint)) |
                                (CourseRegulation.group.contains(course_regulation_constraint)))
                        )
            else:
                found_course_regulations = (
                    CourseRegulation.select().where((CourseRegulation.program.in_(lookup_programs)))
                )
        else:
            if course_regulation_slot:
                course_regulation_constraints = course_regulation_slot.split(" ")
                if len(course_regulation_constraints) == 1:
                    found_course_regulations = (
                        CourseRegulation.select().where((CourseRegulation.name.contains(course_regulation_slot)) |
                                                        (CourseRegulation.group.contains(course_regulation_slot)))
                                                )
                else:
                    found_course_regulations = CourseRegulation.select()
                    for course_regulation_constraint in course_regulation_constraints:
                        found_course_regulations = (
                            found_course_regulations.where(
                                (CourseRegulation.name.contains(course_regulation_constraint)) |
                                (CourseRegulation.group.contains(course_regulation_constraint)))
                        )
            else:
                # HINT: think about this behaviour
                dispatcher.utter_message("Sorry I couldn't extract a Course Regulation "
                                         "from your information, please try again.")
                return [SlotSet("courseRegulationMatch", "zero"),
                        SlotSet("program", None),
                        SlotSet("degree", None),
                        SlotSet("courseRegulation", None)]

        course_regulations_amount = found_course_regulations.count()

        dispatcher.utter_message("I found " + str(found_course_regulations.count()) +
                                 " Course Regulations for your input.")

        if course_regulations_amount == 0:
            course_regulation_match = "zero"
            dispatcher.utter_message("Sorry I couldn't find any Course Regulations. "
                                     "I will reset the found Program and Degree and Course Regulation "
                                     "I extracted from your message")
            return [SlotSet("courseRegulationMatch", course_regulation_match),
                    SlotSet("program", None),
                    SlotSet("degree", None),
                    SlotSet("courseRegulation", None)]

        elif course_regulations_amount == 1:
            course_regulation_match = "one"
            dispatcher.utter_message("Here is the Course Regulation I found: " + found_course_regulations[0].name +
                                     " with the Group: " + str(found_course_regulations[0].group))
        else:
            course_regulation_match = "multiple"
            message = []
            for course_regulation in found_course_regulations:
                message.append(str("Course Regulation: " + course_regulation.name + " Group: " +
                                   course_regulation.group))

            message.insert(0, "Here are the Course Regulations I found:\n")

            dispatcher.utter_message("\n".join(message))

        return [SlotSet("courseRegulationMatch", course_regulation_match)]


class ActionCheckEcts(Action):
    # TODO: implement function to recognize greater than / less than
    def name(self):
        return "action_check_ects"

    def run(self, dispatcher, tracker, domain):
        ects: float = tracker.get_slot("ects")

        if not ects or ects == 0.0:
            dispatcher.utter_message("Sorry I couldn't extract a valid number to contsraint"
                                     " the ects from your message, please try again.")
            return [SlotSet("ectsMatch", "zero"),
                    SlotSet("ects", 0.0)]

        query = MTSModule.select().where(MTSModule.ects == int(ects))
        query_count = query.count()

        if query_count == 0:
            ects_match = "zero"
            dispatcher.utter_message("Sorry I couldn't find any Modules with " + str(int(ects)) + " ECTS. \
                                    I'm resetting your input.")
            return [SlotSet("ectsMatch", ects_match),
                    SlotSet("ects", 0.0)]
        elif query_count == 1:
            ects_match = "one"
        else:
            ects_match = "multiple"

        dispatcher.utter_message("I found " + str(query_count) + " modules with " + str(int(ects)) + " ECTS")

        return [SlotSet("ectsMatch", ects_match)]


class ActionCheckPerson(Action):

    def name(self):
        return "action_check_person"

    def run(self, dispatcher, tracker, domain):
        person: str = tracker.get_slot("person")

        if not person:
            dispatcher.utter_message("Sorry I couldn't extract a valid person name, please try again.")
            return [SlotSet("personMatch", "zero"),
                    SlotSet("personModuleMatchZero", "zero")]

        person_names: list = person.split(" ")
        person_query = None

        if len(person_names) == 1:
            person_name = person_names[0]
            query = Person.select().where(Person.lastname.contains(person_name))
            if query.count() > 0:
                person_query = "lastname"
            else:
                query = Person.select().where(Person.firstname.contains(person_name))
                if query.count() > 0:
                    person_query = "firstname"

        else:
            # Here I'm making the assumption that there are no lastnames consisting of two words
            # and there won't be queries for persons using only multiple firstnames
            person_firstname = " ".join(person_names[0:-1])
            person_lastname = person_names[-1]
            query = Person.select().where((Person.firstname.contains(person_firstname) &
                                           (Person.lastname.contains(person_lastname))))
            if query.count() > 0:
                person_query = "firstnameAndLastname"

        query_count = query.count()

        if query_count == 0:
            person_match = "zero"
            dispatcher.utter_message("Sorry I couldn't find any Persons using the name " + str(person) + ". \
                                    I'm resetting your input.")
            return [SlotSet("personMatch", person_match),
                    SlotSet("personModuleMatch", "zero"),
                    SlotSet("person", None)]
        elif query_count == 1:
            person_match = "one"
        else:
            person_match = "multiple"

        dispatcher.utter_message("I found " + str(query_count) + " Persons with the name " + person + ". ")

        # Now checking if there are Modules taught by the person
        module_query = MTSModule.select().where(MTSModule.responsiblePerson.in_(query))
        module_query_count = module_query.count()
        if module_query_count == 0:
            person_module_match = "zero"
            dispatcher.utter_message("I couldn't find any modules taught by someone with the name" + str(person) + ".")
        elif module_query_count == 1:
            person_module_match = "one"
        else:
            person_module_match = "multiple"

        dispatcher.utter_message("I also found " + str(module_query_count) + " modules taught by " + person + ".")

        return [SlotSet("personMatch", person_match),
                SlotSet("personQuery", person_query),
                SlotSet("personModuleMatch", person_module_match)]


# HINT: keep this updated with all module related slots
module_slots = {
    "moduleTitle": "Module Title",
    "program": "Program",
    "degree": "Degree",
    "courseRegulation": "A Course Regulation",
    "person": "Name of a Responsible Person",
    "ects": "ECTS"
}


class ActionAskForMoreModuleInformation(Action):
    def name(self):
        return "action_ask_for_more_module_information"

    @staticmethod
    def create_message_for_available_information(available_information):
        message = "Here is information I already extracted from our conversation:\n"
        for slot in available_information:
            message += module_slots[slot[0]] + ": " + slot[1] + "\n"

        return message

    @staticmethod
    def create_message_for_possible_information(possible_information):
        message = "Here are some more things you could specify: "
        message += ", ".join(map(lambda slot: module_slots[slot], possible_information))
        return message

    def run(self, dispatcher, tracker, domain):
        available_information = []  # slots that are already filled (should be checked)
        possible_information = []  # slots that could be filled
        for module_slot in module_slots:
            slot_entry = tracker.get_slot(module_slot)
            if slot_entry:
                available_information.append((module_slot, slot_entry))
            else:
                possible_information.append(module_slot)

        message = ""
        if len(available_information) > 0:
            message += self.create_message_for_available_information(available_information)
        if len(possible_information) > 0:
            message += self.create_message_for_possible_information(possible_information)

        dispatcher.utter_message(message)
        return []


class ActionShowFoundPersons(Action):

    def name(self):
        return "action_show_found_persons"

    def run(self, dispatcher, tracker, domain):
        person = tracker.get_slot("person")
        person_match = tracker.get_slot("personMatch")
        person_query = tracker.get_slot("personQuery")

        if not person_match or not person or person_query not in ("firstname", "lastname", "firstnameAndLastname"):
            dispatcher.utter_message("Sorry I couldn't retrieve a person for your information.")
            return []

        person_names: list = person.split(" ")
        if person_query == "firstname":
            persons = Person.select().where(Person.firstname.contains(person_names[0]))
        elif person_query == "lastname":
            persons = Person.select().where(Person.firstname.contains(person_names[0]))
        else:
            person_firstname = " ".join(person_names[0:-1])
            person_lastname = person_names[-1]
            persons = Person.select().where((Person.firstname.contains(person_firstname)) &
                                            (Person.lastname.contains(person_lastname)))
        person_list = []
        for found_person in persons:
            person_list.append(found_person.fullname)

        dispatcher.utter_message("Here are the persons I found for your Information:")
        dispatcher.utter_message("\n".join(person_list))
        dispatcher.utter_message("Can I help you with anything else?")
        return []


class ActionShowFoundModules(Action):
    # TODO: this Action has to do a lot more than it does right now
    # TODO: potentially check only partial information of user to still match a query
    match_slots = {"moduleTitleMatch", "courseRegulationMatch", "personModuleMatch", "ectsMatch"}

    def name(self):
        return "action_show_found_modules"

    @staticmethod
    def lookup_module_title(query, module_title, module_title_exact_match):
        if not module_title and type(module_title) != str:
            raise KeyError("moduleTitle-Slot shouldn't be empty")
        if module_title_exact_match:
            query = query.select().where(MTSModule.title ** module_title)
        else:
            query = query.select().where(MTSModule.title.contains(module_title))

        return query

    @staticmethod
    def lookup_program_and_course_regulation(query, program, degree, program_match,
                                             program_exact_match, course_regulation):
        lookup_programs = None
        if program_match in {"one", "multiple"}:
            if program and degree:
                lookup_programs = Program.select().where((Program.name.contains(program)) &
                                                         (Program.degree.contains(degree)))
            elif program:
                if program_exact_match:
                    lookup_programs = Program.select().where(Program.name ** program)
                else:
                    lookup_programs = Program.select().where(Program.name.contains(program))
            elif degree:
                lookup_programs = Program.select().where(Program.degree.contains(degree))
            else:
                raise KeyError("program- and degree-Slot shouldn't be empty")

        if lookup_programs:
            if course_regulation:
                lookup_course_regulations = (
                    CourseRegulation.select().where((CourseRegulation.program.in_(lookup_programs)))
                )
                course_regulation_constraints = course_regulation.split(" ")
                if len(course_regulation_constraints) == 1:
                    lookup_course_regulations = (
                        lookup_course_regulations.where((CourseRegulation.name.contains(course_regulation)) |
                                                        (CourseRegulation.group.contains(course_regulation)))
                                                )
                else:
                    for course_regulation_constraint in course_regulation_constraints:
                        lookup_course_regulations = (
                            lookup_course_regulations.where(
                                (CourseRegulation.name.contains(course_regulation_constraint)) |
                                (CourseRegulation.group.contains(course_regulation_constraint)))
                        )
            else:
                lookup_course_regulations = CourseRegulation.select().where((CourseRegulation.program
                                                                             .in_(lookup_programs)))
        else:
            if course_regulation:
                course_regulation_constraints = course_regulation.split(" ")
                if len(course_regulation_constraints) == 1:
                    lookup_course_regulations = (
                        CourseRegulation.select().where((CourseRegulation.name.contains(course_regulation)) |
                                                        (CourseRegulation.group.contains(course_regulation)))
                                                )
                else:
                    lookup_course_regulations = CourseRegulation.select()
                    for course_regulation_constraint in course_regulation_constraints:
                        lookup_course_regulations = (
                            lookup_course_regulations.where(
                                (CourseRegulation.name.contains(course_regulation_constraint)) |
                                (CourseRegulation.group.contains(course_regulation_constraint)))
                        )
            else:
                raise KeyError("courseRegulation-Slot shouldn't be empty if program- and degree-Slot are")

        module_ids_from_lookup_course_regulations = (MTSModuleCourseRegulations
                                                     .select(MTSModuleCourseRegulations.mtsmodule).distinct()
                                                     .where(MTSModuleCourseRegulations.courseregulation
                                                            .in_(lookup_course_regulations)))

        query = query.select().where(MTSModule.id.in_(module_ids_from_lookup_course_regulations))
        return query

    @staticmethod
    def lookup_ects(query, ects):
        if not ects and type(ects) != float:
            raise KeyError("ects-Slot shouldn't be empty")
        query = query.select().where(MTSModule.ects == int(ects))

        return query

    @staticmethod
    def lookup_person(query, person, person_query):
        person_names: list = person.split(" ")
        if person_query == "firstname":
            persons = Person.select().where(Person.firstname.contains(person_names[0]))
        elif person_query == "lastname":
            persons = Person.select().where(Person.lastname.contains(person_names[0]))
        else:
            person_firstname = " ".join(person_names[0:-1])
            person_lastname = person_names[-1]
            persons = Person.select().where((Person.firstname.contains(person_firstname)) &
                                            (Person.lastname.contains(person_lastname)))
        query = query.select().where(MTSModule.responsiblePerson.in_(persons))

        return query

    def retry_query_with_less_lookups(self, tracker, used_match_slots, combination_amount):
        if combination_amount == 0:
            return None

        new_possible_lookups = itertools.combinations(used_match_slots, combination_amount)

        for new_possible_lookup in new_possible_lookups:
            query = MTSModule.select()
            used_information = []

            if "moduleTitleMatch" in new_possible_lookup:
                module_title: str = tracker.get_slot("moduleTitle")
                module_title_exact_match: bool = tracker.get_slot("moduleTitleExactMatch")

                query = self.lookup_module_title(query, module_title, module_title_exact_match)
                used_information.append("moduleTitle")

            if "courseRegulationMatch" in new_possible_lookup:
                program: str = tracker.get_slot("program")
                degree: str = tracker.get_slot("degree")
                program_match = tracker.get_slot("programMatch")
                program_exact_match: bool = tracker.get_slot("programExactMatch")
                course_regulation: str = tracker.get_slot("courseRegulation")

                query = self.lookup_program_and_course_regulation(query, program, degree, program_match,
                                                                  program_exact_match, course_regulation)
                used_information.append("courseRegulation")

            if "personModuleMatch" in new_possible_lookup:
                person = tracker.get_slot("person")
                person_query = tracker.get_slot("personQuery")

                if person_query in ("firstname", "lastname", "firstnameAndLastname"):
                    query = self.lookup_person(query, person, person_query)
                    used_information.append("person")

            if "ectsMatch" in new_possible_lookup:
                ects: float = tracker.get_slot("ects")

                query = self.lookup_ects(query, ects)
                used_information.append("ects")

            query_count = query.count()
            if query_count > 0:
                return query, used_information

        return self.retry_query_with_less_lookups(tracker, used_match_slots, combination_amount - 1)

    def run(self, dispatcher, tracker, domain):
        query: ModelSelect = MTSModule.select()

        # LOOKUP for moduleTitle
        if tracker.get_slot("moduleTitleMatch") in ("one", "multiple"):
            module_title: str = tracker.get_slot("moduleTitle")
            module_title_exact_match: bool = tracker.get_slot("moduleTitleExactMatch")

            query = self.lookup_module_title(query, module_title, module_title_exact_match)

        # LOOKUP for program and courseRegulation
        if tracker.get_slot("courseRegulationMatch") in {"one", "multiple"}:
            program: str = tracker.get_slot("program")
            degree: str = tracker.get_slot("degree")
            program_match = tracker.get_slot("programMatch")
            program_exact_match: bool = tracker.get_slot("programExactMatch")
            course_regulation: str = tracker.get_slot("courseRegulation")

            query = self.lookup_program_and_course_regulation(query, program, degree, program_match,
                                                              program_exact_match, course_regulation)

        # LOOKUP for person
        if tracker.get_slot("personModuleMatch") in ("one", "multiple"):
            person = tracker.get_slot("person")
            person_query = tracker.get_slot("personQuery")

            if person_query in ("firstname", "lastname", "firstnameAndLastname"):
                query = self.lookup_person(query, person, person_query)

        # LOOKUP for ects
        if tracker.get_slot("ectsMatch") in ("one", "multiple"):
            ects: float = tracker.get_slot("ects")

            query = self.lookup_ects(query, ects)

        # FEATURE: Add more things to constraint query
        query_count = query.count()

        used_module_slots = None
        if query_count == 0:
            used_match_slots = []
            for match_slot in self.match_slots:
                if tracker.get_slot(match_slot) in ("one", "multiple"):
                    used_match_slots.append(match_slot)

            if used_match_slots in (0, 1):
                dispatcher.utter_message("I couldn't find any results for your query")
                return [Restarted(), AllSlotsReset()]

            else:
                dispatcher.utter_message("I couldn't find any modules for your information but I'm trying to find"
                                         " one using part of it.")
                combination_amount = len(used_match_slots) - 1
                query = self.retry_query_with_less_lookups(tracker, used_match_slots, combination_amount)[0]
                used_module_slots = self.retry_query_with_less_lookups(tracker, used_match_slots, combination_amount)[1]

                if query is None:
                    dispatcher.utter_message("I couldn't find any results for your query")
                    return [Restarted(), AllSlotsReset()]
                query_count = query.count()

        # displaying amount of found modules
        dispatcher.utter_message("I found " + str(query_count) + " modules using the following information:")

        # displaying used slots
        message = []
        used_slots = []
        for module_slot in (module_slots if not used_module_slots else used_module_slots):
            slot_entry = tracker.get_slot(module_slot)
            if slot_entry:
                used_slots.append((module_slot, slot_entry))

        for slot in used_slots:
            message.append(str(module_slots[slot[0]] + ": " + str(slot[1])))
        dispatcher.utter_message("\n".join(message))

        # displaying modules themselves
        module_message = []
        for index, module in enumerate(query):
            if index < 10:
                module_message.append((str(module.title) + ":" +
                                       "\nResponsible Person: " + str(module.responsiblePerson.fullname) +
                                       "\nECTS: " + str(module.ects) +
                                       "\nWebsite: " + str(module.website)))
            else:
                module_message.insert(0, "Here are the first 10 modules")
                break
        dispatcher.utter_message("\n\n".join(module_message))
        dispatcher.utter_message("Can I help you with anything else?")
        return []
