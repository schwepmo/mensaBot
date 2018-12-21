## mensa_search_000
* show_mensa_data
    - action_show_mensa_data
    
## mensa_search_000_1
* show_mensa_data{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - action_show_mensa_data
    
## mensa_search_000_2
* show_mensa_menu{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - action_show_mensa_menu
    
## mensa_search_001_a
* inform_mensa{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "multiple"}
    - action_ask_for_more_mensa_information

## mensa_search_001_b
* inform_mensa{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - utter_ask_show_mensa_information
* add_more_mensa_information
    - action_ask_for_more_mensa_information

## mensa_search_001_b
* inform_mensa{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - utter_ask_show_mensa_information
* show_mensa_data
    - action_show_mensa_data

## mensa_search_001_b
* inform_mensa{"mensaName": "hardenberg"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - utter_ask_show_mensa_information
* show_mensa_menu
    - action_show_mensa_menu

## mensa_search_002
* inform_mensa{"price": 5.0}
    - action_check_price
    - action_ask_for_more_mensa_information
    
## mensa_search_003
* inform_mensa{"menuCourse": "dessert"}
    - action_check_menu_course
    - action_ask_for_more_mensa_information 
       
## mensa_search_004
* inform_mensa{"mensaName": "hardenberg", "price": 5.0}
    - action_check_mensa_names
    - slot{"mensaMatch": "multiple"}
    - action_check_price
    - action_ask_for_more_mensa_information
    
## mensa_search_005
* inform_mensa{"mensaName": "hardenberg", "menuCourse": "dessert"}
    - action_check_mensa_names
    - slot{"mensaMatch": "multiple"}
    - action_check_menu_course
    - action_ask_for_more_mensa_information

## mensa_search_006
* inform_mensa{"price": 5.0, "menuCourse": "dessert"}
    - action_check_price
    - action_check_menu_course
    - action_ask_for_more_mensa_information
    
## mensa_search_007
* inform_mensa{"mensaName": "hardenberg", "price": 5.0, "menuCourse": "dessert"}
    - action_check_mensa_names
    - slot{"mensaMatch": "multiple"}
    - action_check_price
    - action_check_menu_course
    - action_ask_for_more_mensa_information
    
## mensa_search_008
* set_context_mensa
    - action_set_context_mensa
* inform_mensa{"mensaName": "Hardenbergmensa"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - utter_ask_show_mensa_information
* show_mensa_data
    - action_show_mensa_data

## menu_search_000
* show_mensa_menu
    - action_show_mensa_menu

## menus_search_000_1
* inform_vegetarian_true
    - action_set_vegetarian_true
    - slot{"vegetarian": 1}
## menus_search_000_2
* inform_vegan_true
    - action_set_vegan_true
    - slot{"vegan": 1}
        
## menus_search_000_3
* reset_food_restrictions
    - action_reset_food_restrictions
       
## menu_search_001
* set_context_mensa
    - action_set_context_mensa
* inform_vegetarian_true
    - action_set_vegetarian_true
    - slot{"vegetarian": 1}
    - utter_ask_show_mensa_information
* add_more_mensa_information
    - action_ask_for_more_mensa_information
* inform_mensa{"mensaName": "Hardenbergmensa"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - action_ask_for_more_mensa_information
* inform_mensa{"price": 5.00}
    - action_check_price
    - slot{"price": 5.00}
    - utter_ask_show_mensa_information
* show_mensa_menu
    - action_show_mensa_menu
  
## menu_search_002
* set_context_mensa
    - action_set_context_mensa
* inform_mensa{"mensaName": "Hardenbergmensa"}
    - action_check_mensa_names
    - slot{"mensaMatch": "one"}
    - utter_ask_show_mensa_information
* show_mensa_menu
    - action_show_mensa_menu