# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from tensorflow.python.platform import self_check

from actions.ml_model import get_slots_using_location


class AskSlotInfo(Action):
    def name(self) -> Text:
        print("===> hit AskSlotInfo")
        return "return_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskSlotInfo - run")
        dispatcher.utter_message(json_message=tracker.slots)
        return []


class AskNameAndGender(Action):
    def name(self) -> Text:
        print("===> hit AskNameAndGender")
        return "action_ask_name_and_gender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskNameAndGender - run")

        # dispatcher.utter_message(text="tell name and gender")
        elements = {
            "payload": {
                "mainTitle": "Let's get to know you better.",
                "questionScreenType": 1,
                "questions": [
                    {
                        "qzOrder": 1,
                        "qzTitle": "Full name",
                        "qzType": "text",
                        "answers": []
                    },
                    {
                        "qzOrder": 2,
                        "qzTitle": "Gender",
                        "qzType": "mcq",
                        "answers": [
                            "Male",
                            "Female",
                            "Non-binary",
                            "Rather not say"
                        ]
                    }
                ]

            }
        }
        dispatcher.utter_message(json_message=elements)

        return []


class AskNameAndGenderSubmit(Action):
    def name(self) -> Text:
        print("===> hit AskNameAndGenderSubmit")
        return "action_ask_name_and_gender_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[SlotSet]:
        print("===> hit AskNameAndGenderSubmit - run")

        text = tracker.latest_message['text']

        data = json.loads(text.split("@")[1].strip())

        name = data['name']
        gender = data['gender']

        dispatcher.utter_message(text="Name gender saved in a slot")

        return [SlotSet("name", name), SlotSet("gender", gender)]


class AskBasicQZ(Action):
    def name(self) -> Text:
        print("===> hit AskBasicQZ")
        return "action_ask_basic_qz"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskBasicQZ - run")

        # dispatcher.utter_message(text="Hello World!")
        elements = {
            "payload": {
                "mainTitle": "A few basics  to get a baseline started for you.",
                "questionScreenType": 2,
                "questions": [
                    {
                        "qzOrder": 1,
                        "qzTitle": "Age",
                        "qzValueUnit": "int",
                        "qzValueType": "years",
                        "qzType": "text",
                        "answers": []
                    },
                    {
                        "qzOrder": 2,
                        "qzTitle": "Height",
                        "qzValueUnit": "int",
                        "qzValueType": "length",
                        "qzType": "text",
                        "answers": []
                    },
                    {
                        "qzOrder": 3,
                        "qzTitle": "Weight",
                        "qzValueUnit": "int",
                        "qzValueType": "weight",
                        "qzType": "text",
                        "answers": []
                    },
                    {
                        "qzOrder": 4,
                        "qzTitle": "Waist Circumference",
                        "qzValueUnit": "int",
                        "qzValueType": "length",
                        "qzType": "text",
                        "answers": []
                    }
                ]

            }
        }
        dispatcher.utter_message(json_message=elements)

        return []


class AskBasicQZSubmit(Action):
    def name(self) -> Text:
        print("===> hit AskBasicQZSubmit")
        return "action_ask_basic_qz_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskBasicQZ - run")

        text = tracker.latest_message['text']

        data = json.loads(text.split("@")[1].strip())

        age = data['age']
        height = data['height']
        height_unit = data['height_unit']
        weight = data['weight']
        weight_unit = data['weight_unit']
        waist_circumference = data['waist_circumference']
        waist_circumference_unit = data['waist_circumference_unit']

        dispatcher.utter_message(text="Age height weight saved successfully")

        return [
            SlotSet("age", age),
            SlotSet("height", height),
            SlotSet("height_unit", height_unit),
            SlotSet("weight", weight),
            SlotSet("weight_unit", weight_unit),
            SlotSet("waist_circumference", waist_circumference),
            SlotSet("waist_circumference_unit", waist_circumference_unit)
        ]


class AskLocation(Action):
    def name(self) -> Text:
        print("===> hit AskLocation")
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskLocation - run")

        # dispatcher.utter_message(text="Hello World!")
        elements = {
            "payload": {
                "mainTitle": "Your geographic region will tell us a lot about the opportunities for physical activity in your region.",
                "questionScreenType": 3,
                "questions": [
                    {
                        "qzOrder": 1,
                        "qzTitle": "Location",
                        "qzValueUnit": "",
                        "qzValueType": "countries",
                        "qzType": "text",
                        "answers": []
                    }
                ]

            }
        }
        dispatcher.utter_message(json_message=elements)

        return []


class AskLocationSubmit(Action):
    def name(self) -> Text:
        print("===> hit AskLocationSubmit")
        return "action_ask_location_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskLocationSubmit - run")

        text = tracker.latest_message['text']

        data = json.loads(text.split("@")[1].strip())

        location = data['location']

        print(location)

        has_swim_facility, has_walking_facility = get_slots_using_location(location)

        print(has_swim_facility, has_walking_facility)
        dispatcher.utter_message("Location data saved")

        return [
            SlotSet("location", location),
            SlotSet("has_swim_facility", True if has_swim_facility else False),
            SlotSet("has_walking_facility", True if has_walking_facility else False)
        ]


class AskSwimmingInfo(Action):
    def name(self) -> Text:
        print("===> hit AskSwimmingInfo")
        return "action_ask_swimming_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskSwimmingInfo - run")

        # dispatcher.utter_message(text="Hello World!")
        elements = {
            "payload": {
                "mainTitle": "How many times you swim within a week and how long for once?",
                "questionScreenType": 3,
                "questions": [
                    {
                        "qzOrder": 1,
                        "qzTitle": "Swimming Count for a week",
                        "qzValueUnit": "",
                        "qzValueType": "swim_count",
                        "qzType": "text",
                        "answers": []
                    },
                    {
                        "qzOrder": 2,
                        "qzTitle": "How long at once",
                        "qzValueUnit": "",
                        "qzValueType": "swim_hours",
                        "qzType": "text",
                        "answers": []
                    }
                ]

            }
        }
        dispatcher.utter_message(json_message=elements)

        return []


class AskSwimmingInfoSubmit(Action):
    def name(self) -> Text:
        print("===> hit AskSwimmingInfoSubmit")
        return "action_ask_swimming_info_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskSwimmingInfoSubmit - run")

        text = tracker.latest_message['text']

        data = json.loads(text.split("@")[1].strip())

        return [
            SlotSet("swim_count_within_week", data['swim_count_within_week']),
            SlotSet("swim_hours_at_once", data['swim_hours_at_once'])
        ]


class AskJoggingInfo(Action):
    def name(self) -> Text:
        print("===> hit AskJoggingInfo")
        return "action_ask_jogging_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("===> hit AskJoggingInfo - run")

        # dispatcher.utter_message(text="Hello World!")
        # elements = {
        #     "payload": {
        #         "mainTitle": "How many times you swim within a week and how long for once?",
        #         "questionScreenType": 3,
        #         "questions": [
        #             {
        #                 "qzOrder": 1,
        #                 "qzTitle": "Swimming Count for a week",
        #                 "qzValueUnit": "",
        #                 "qzValueType": "swim_count",
        #                 "qzType": "text",
        #                 "answers": []
        #             },
        #             {
        #                 "qzOrder": 2,
        #                 "qzTitle": "How long at once",
        #                 "qzValueUnit": "",
        #                 "qzValueType": "swim_hours",
        #                 "qzType": "text",
        #                 "answers": []
        #             }
        #         ]
        #
        #     }
        # }
        # dispatcher.utter_message(json_message=elements)
        dispatcher.utter_message("Jogging qs not implemented yet")

        return []
# class AskAboutPhysicalActivity(Action):
#     def name(self) -> Text:
#         print("===> hit AskAboutPhysicalActivity")
#         return "action_ask_about_physical_activity"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         print("===> hit AskAboutPhysicalActivity - run")
#
#         # dispatcher.utter_message(text="Hello World!")
#         elements = {
#             "payload": {
#                 "mainTitle": "How many times do you engage in physical activity a week?",
#                 "note": "For this measure please ensure there is sufficiently prolonged and intense to cause sweating and a rapid heart beat,",
#                 "questionScreenType": 4,
#                 "questions": [
#                     {
#                         "qzOrder": 1,
#                         "qzTitle": "",
#                         "qzValueUnit": "",
#                         "qzValueType": "countries",
#                         "qzType": "mcq",
#                         "answers": [
#                             {"answerText": "At least 3 times", "orderID": 1},
#                             {"answerText": "Normally once or twice", "orderID": 2},
#                             {"answerText": "Rarely or never", "orderID": 3}
#                         ]
#                     }
#                 ]
#
#             }
#         }
#         dispatcher.utter_message(json_message=elements)
#
#         return []
#
#
# class WeightQZ(Action):
#
#     def name(self) -> Text:
#         print("===> hit WeightQZ")
#         return "weight_qz_action"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         print("===> hit WeightQZ - run")
#
#         # dispatcher.utter_message(text="Hello World!")
#         elements = {
#             "payload": {
#                 "mainTitle": "Weight Questions",
#                 "questionScreenType": 1,
#                 "questions": [
#                     {
#                         "qzTitle": "",
#                         "qzType": "mcq",
#                         "answers": [
#                             "Lighly active",
#                             "Active",
#                             "Athlete",
#                             "Heavy duty professinal",
#                             "Not active at all"
#                         ]
#                     }
#                 ]
#
#             }
#         }
#         dispatcher.utter_message(json_message=elements)
#
#         return []



