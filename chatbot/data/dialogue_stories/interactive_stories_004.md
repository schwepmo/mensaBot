## Generated Story 6965247593337420421
* inform_mensa{"mensaName": "hardenberg"}
    - slot{"mensaName": ["hardenberg"]}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - slot{"mensaName": ["hardenberg"]}
    - action_ask_for_more_mensa_information
* inform_vegan_true
    - action_set_vegan_true
    - slot{"vegan": true}
    - action_ask_for_more_mensa_information
* show_mensa_data
    - action_show_mensa_data
* show_mensa_menu
    - action_show_mensa_menu
* set_context_module
    - action_set_context_module
    - slot{"mensaName": null}
    - slot{"menuCourse": null}
    - slot{"price": 0.0}
    - slot{"vegetarian": false}
    - slot{"vegan": false}
    - slot{"mensaMatch": null}
* inform_module{"ects": "9"}
    - slot{"ects": "9"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - action_ask_for_more_module_information
* inform_module{"person": "m\u00f6ller"}
    - slot{"person": "m\u00f6ller"}
    - action_check_person
    - slot{"personMatch": "multiple"}
    - slot{"personQuery": "lastname"}
    - slot{"personModuleMatch": "multiple"}
    - action_ask_for_more_module_information
* show_found_modules
    - action_show_found_modules
* set_context_module{"moduleTitle": "Dititale Systeme"}
    - slot{"moduleTitle": "Dititale Systeme"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "zero"}
    - slot{"moduleTitle": null}
    - action_ask_for_more_module_information
* set_context_module{"moduleTitle": "Digitale Systeme"}
    - slot{"moduleTitle": "Digitale Systeme"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "one"}
    - slot{"moduleTitleExactMatch": true}
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
* show_mensa_menu{"mensaName": "skyline cafe"}
    - slot{"mensaName": ["skyline cafe"]}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - slot{"mensaName": ["skyline cafe"]}
    - action_show_mensa_menu
* inform_mensa{"price": "5,00"}
    - slot{"price": "5,00"}
    - action_check_price
    - slot{"price": 5.0}
    - action_ask_for_more_mensa_information
* inform_mensa{"price": "5,00"}
    - slot{"price": "5,00"}
    - action_check_price
    - slot{"price": 5.0}
    - action_ask_for_more_mensa_information
* show_mensa_data
    - action_show_mensa_data

