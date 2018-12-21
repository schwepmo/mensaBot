## Generated Story 114830680094403003
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
* inform_mensa{"mensaName": "Mar"}
    - slot{"mensaName": ["Hardenberg", "Mar"]}
    - action_check_mensa_names
    - slot{"mensaMatch": "multiple"}
    - slot{"mensaName": ["Hardenberg", "Mar"]}
    - action_ask_for_more_mensa_information
* show_mensa_data
    - action_show_mensa_data
* inform_mensa{"mensaName": "Mar"}
    - slot{"mensaName": ["Hardenberg", "Mar"]}
    - action_check_mensa_names
    - action_ask_for_more_mensa_information
* inform_mensa{"menuCourse": "aktion"}
    - slot{"menuCourse": ["aktion"]}
    - action_check_menu_course
    - action_ask_for_more_mensa_information
* show_mensa_menu
    - action_show_mensa_menu
* inform_module{"courseRegulation": "Technische Informatik"}
    - slot{"courseRegulation": "Technische Informatik"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - action_ask_for_more_module_information
* inform_module{"moduleTitle": "Analysis"}
    - slot{"moduleTitle": "Analysis"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "multiple"}
    - slot{"moduleTitleExactMatch": false}
    - action_ask_for_more_module_information
* show_found_modules
    - action_show_found_modules
* inform_module{"moduleTitle": "Digitale Systeme"}
    - slot{"moduleTitle": "Digitale Systeme"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "one"}
    - slot{"moduleTitleExactMatch": true}
    - action_show_found_modules

