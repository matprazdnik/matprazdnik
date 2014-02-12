keep in mind:
    http://django-tables2.readthedocs.org/en/latest/index.html


general issues:
    filter
    add_new_button with default settings
    tab_index, onenterpress, onescapepress


general features:
    sort_by


ideas:
    stop polling server for new rows while editing a row
    poll to load new rows (1 time per second)
    # poll to reload everything (1 time per minute)


schools
    School
        name:
        city: search_hint
        genitiv: auto_generate(param: js_code)


participants
    Participant
        reg_number: validate(param: js_code)
        surname, name
        grade: default value
        school: foreign_key
            how to represent? function which composes text
            how to change? change current, add new


points
    Participant
        points: editing entry point
        comma separated integers columns
        autosum: complicated validation based on all current-row information


diplomas
    Participant



let flying_rows save history of changes by ip
Participant
    id                                     created     changed
    57       127.0.0.17 (12th creature of this ip)       never
