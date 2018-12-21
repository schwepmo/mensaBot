## module_search_000_0
* show_found_modules
    - action_show_found_modules

## module_search_001
* inform_module{"moduleTitle": "Digitale Systeme"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "one"}
    - action_show_found_modules

## module_search_002
* inform_module{"moduleTitle": "Digitale Systeme"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "multiple"}
    - action_ask_for_more_module_information

## module_search_003
* inform_module{"ects": 9.0}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - action_ask_for_more_module_information

## module_search_004_a
* inform_module{"person": "Sebastian Möller"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "one"}
    - action_show_found_modules
    
## module_search_004_b
* inform_module{"person": "Sebastian Möller"}
    - action_check_person
    - slot{"personMatch": "one", "personModuleMatch": "one"}
    - action_show_found_modules
    
 ## module_search_004_c
* inform_module{"person": "Sebastian Möller"}
    - action_check_person
    - slot{"personMatch": "one", "personModuleMatch": "multiple"}
    - action_ask_for_more_module_information

## module_search_005_a
* inform_module{"courseRegulation": "Technische Informatik 2015"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_005_b
* inform_module{"courseRegulation": "Technische Informatik 2015"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_005_c
* inform_module{"courseRegulation": "Technische Informatik 2015"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "zero", "courseRegulation": null, "program": null, "degree": null}
    
* show_found_modules
    - action_show_found_modules
## module_search_006_a
* inform_module{"program": "Technische Informatik"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_006_b
* inform_module{"program": "Technische Informatik"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_006_c
* inform_module{"program": "Technische Informatik"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_ask_for_more_module_information

## module_search_006_d
* inform_module{"degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_006_e
* inform_module{"degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_006_f
* inform_module{"degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_ask_for_more_module_information
    
## module_search_006_g
* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_006_h
* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "one"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_006_i
* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_ask_for_more_module_information

## module_search_007_a
* inform_module{"program": "Technische Informatik", "ects": 6.0}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_007_b
* inform_module{"program": "Technische Informatik", "ects": 6.0}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_007_c
* inform_module{"program": "Technische Informatik", "degree": "Bachelor" , "ects": 6.0}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_007_d
* inform_module{"program": "Technische Informatik", "degree": "Bachelor" , "ects": 6.0}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules
    
## module_search_008_a
* inform_module{"courseRegulation": "Technische Informatik", "ects": 6.0}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_008_b
* inform_module{"courseRegulation": "Technische Informatik", "ects": 6.0}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - action_check_ects
    - slot{"ectsMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules
    
## module_search_009_a
* inform_module{"program": "Technische Informatik", "person": "Möller"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_009_b
* inform_module{"program": "Technische Informatik", "person": "Möller"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## module_search_009_c
* inform_module{"program": "Technische Informatik", "degree": "Bachelor" , "person": "Möller"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_009_d
* inform_module{"program": "Technische Informatik", "degree": "Bachelor" , "person": "Möller"}
    - action_check_program
    - slot{"programMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules
    
## module_search_010_a
* inform_module{"courseRegulation": "Technische Informatik", "person": "Möller"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information

## module_search_010_b
* inform_module{"courseRegulation": "Technische Informatik", "person": "Möller"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - action_check_person
    - slot{"personMatch": "multiple", "personModuleMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules

## person_search_000
* show_found_persons
    - action_show_found_persons

## person_search_001
* inform_module{"person": "Sebastian Möller"}
    - action_check_person
    - slot{"personMatch": "one", "personModuleMatch": "multiple"}
    - action_show_found_modules

## program_courseRegulation_moduleTitle_000
* set_context_module
    - action_set_context_module
    - action_ask_for_more_module_information
* inform_module{"program": "Technische Informatik"}
    - action_check_program
    - slot{"programMatch": "multiple"}
* inform_module{"degree": "Bachelor"}
    - action_check_program
    - slot{"programMatch": "one"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
* inform_module{"courseRegulation": "2015"}
    - action_check_course_regulations
    - slot{"courseRegulationMatch": "multiple"}
    - utter_ask_show_found_modules
* choose_add_more_module_information
    - action_ask_for_more_module_information
* inform_module{"moduleTitle": "Analysis"}
    - action_check_module_title
    - slot{"moduleTitleMatch": "multiple"}
    - utter_ask_show_found_modules
* show_found_modules
    - action_show_found_modules
##   
## ## test_example_001
## * set_context_module
##     - action_set_context_mensa
##     - action_ask_for_more_module_information
## * inform_module{"program": "Technische Informatik"}
##     - action_check_program
##     - slot{"programMatch": "multiple"}
## * inform_module{"degree": "Bachelor"}
##     - action_check_program
##     - slot{"programMatch": "one"}
##     - action_check_course_regulationss
##     - slot{"courseRegulationMatch": "zero"}
##     - action_ask_for_more_module_information
  
#### module_search_000
##* set_context_module
##    - action_ask_for_more_module_information
##* inform_module{"moduleTitle": "Analysis"}
##    - action_check_module_title
##    - slot{"moduleTitleMatch": "multiple"}
##    - utter_ask_show_found_modules
##* show_found_modules
##    - action_show_found_modules 
##    
#### module_search_000_1
##* set_context_module
##    - action_ask_for_more_module_information
##* inform_module{"moduleTitle": "Analysis I"}
##    - action_check_module_title
##    - slot{"moduleTitleMatch": "multiple"}
##    - utter_ask_show_found_modules
##* choose_add_more_module_information
##    - action_ask_for_more_module_information
##* inform_module{"program": "Technische Informatik"}
##    - action_check_program
##    - slot{"programMatch": "zero"}
##    - action_ask_for_more_module_information
## 
#### module_search_001
##* set_context_module
##    - action_ask_for_more_module_information
##* inform_module{"moduleTitle": "Analysis"}
##    - action_check_module_title
##    - slot{"moduleTitleMatch": "one"}
##    - action_show_found_modules
##    - action_reset_dialogue
##
#### module_search_002
##* set_context_module
##    - action_ask_for_more_module_information
##* inform_module{"moduleTitle": "Analysis"}
##    - action_check_module_title
##    - slot{"moduleTitleMatch": "zero"}
##    - action_ask_for_more_module_information
##        
#### module_search_003_program_001_01
##* inform_module{"program": "Technische Informatik"}
##    - action_check_program
##    - slot{"programMatch": "zero"}
##    - slot{"program": "None", "degree": "None"}
##    
#### module_search_003_program_001_02
##* inform_module{"degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "zero"}
##    - slot{"program": "None", "degree": "None"}
##    
#### module_search_003_program_002_01
##* inform_module{"program": "Technische Informatik"}
##    - action_check_program
##    - slot{"programMatch": "multiple"}
##* inform_module{"degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "multiple"}
##    
#### module_search_003_program_002_02
##* inform_module{"program": "Technische Informatik"}
##    - action_check_program
##    - slot{"programMatch": "multiple"}
##* inform_module{"degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "one"}
##    - action_check_course_regulationss
##    
#### module_search_003_program_002_03
##* inform_module{"program": "Technische Informatik"}
##    - action_check_program
##    - slot{"programMatch": "multiple"}
##* inform_module{"degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "zero"}
##    - action_ask_for_more_module_information
##    
#### module_search_003_program_003_01
##* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "multiple"}
##    - action_check_course_regulationss
##    - slot{"courseRegulationMatch": "zero"}
##    - action_ask_for_more_module_information
##
#### module_search_003_program_003_02
##* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "one"}
##    - action_check_course_regulationss
##    - slot{"courseRegulationMatch": "multiple"}
##
#### module_search_003_program_003_03
##* inform_module{"program": "Technische Informatik", "degree": "Bachelor"}
##    - action_check_program
##    - slot{"programMatch": "zero"}
     
## ## module_search_001
## * inform_module_person{"personFirstName": "Reinhard", "personLastName": "Nabben"}
##     - action_person_search
## 
##     - action_module_search
##     
## ## module_search_002
## * inform_module{"moduleTitle": "Analysis"}
## 
## ## module_search_003
## * inform{"firstName": "bla"}

## ## testing
## * inform_module{"courseRegulation": "Technische Informatik", "moduleTitle": "Digitale Systeme", "person": "Möller", "ects": 9}
##     - action_check_course_regulationss
##     - slot{"courseRegulationMatch": "multiple"}
##     - action_check_module_title
##     - slot{"moduleTitleMatch": "multiple"}
##     - action_check_person
##     - slot{"personMatch": "multiple"}
##     - slot{"personModuleMatch": "multiple"}
##     - action_check_ects
##     - slot{"ectsMatch": "multiple"}
##     - action_show_found_modules