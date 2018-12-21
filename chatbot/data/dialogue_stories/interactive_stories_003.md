## Generated Story 8801336852735234213
* inform_module
    - action_check_program
    - slot{"programMatch": "zero"}
    - slot{"program": null}
    - slot{"degree": null}
* inform_module{"program": "technische informatik"}
    - slot{"program": "technische informatik"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - slot{"programExactMatch": true}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
* inform_module{"moduleTitle": "modules in my stupo 2015"}
    - slot{"moduleTitle": "modules in my stupo 2015"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "zero"}
    - slot{"moduleTitle": null}
    - action_ask_for_more_module_information
* inform_module{"courseRegulation": "2015"}
    - slot{"courseRegulation": "2015"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules
* set_context_mensa
    - action_set_context_mensa
    - slot{"moduleTitle": null}
    - slot{"program": null}
    - slot{"ects": 0.0}
    - slot{"courseRegulation": null}
    - slot{"degree": null}
    - slot{"moduleTitleMatch": null}
    - slot{"moduleTitleExactMatch": false}
    - slot{"programExactMatch": false}
    - slot{"programMatch": null}
    - slot{"personQuery": null}
    - slot{"personMatch": null}
    - slot{"personModuleMatch": null}
    - slot{"ectsMatch": null}
* set_context_mensa{"mensaName": "mar"}
    - slot{"mensaName": ["mar"]}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - slot{"mensaName": ["mar"]}
    - utter_ask_show_mensa_information
* show_mensa_menu
    - action_show_mensa_menu
* inform_vegan_true
    - action_set_vegan_true
    - slot{"vegan": true}
* show_mensa_menu
    - action_show_mensa_menu
* inform_vegetarian_true
    - action_set_vegetarian_true
    - slot{"vegetarian": true}
* inform_vegan_true
    - action_set_vegan_true
    - slot{"vegan": true}
* reset_food_restrictions
    - action_reset_food_restrictions
    - slot{"vegan": false}
    - slot{"vegetarian": false}
* add_more_mensa_information
    - action_ask_for_more_mensa_information
* inform_mensa{"menuCourse": "aktionen"}
    - slot{"menuCourse": ["aktionen"]}
    - action_check_menu_course
    - slot{"menuCourse": ["Aktionen"]}
    - action_ask_for_more_mensa_information
* inform_mensa{"price": "5,00"}
    - slot{"price": "5,00"}
    - action_check_price
    - slot{"price": 5.0}
    - action_ask_for_more_mensa_information
* show_mensa_menu
    - action_show_mensa_menu

