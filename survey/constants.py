"""
This file contains various constants used throughout the module.
These constants define the maximum and minimum length and question types
"""
MAX_LENGTH = {
    'form_name': 20,
    'description': 200,
    'block_name': 50,
    'name': 50,
    'question': 200,
    'type': 10,
    'choice': 10,

}
MIN_LENGTH = {
    'form_name': 5,
    'description': 10,
    'block_name': 5,
    'question': 5,
    'name': 5,
    'type': 4,
    'choice': 1,

}
TEXT = 'text'
RADIO = 'radio'
CHECKBOX = 'checkbox'

QUESTION_TYPES = [
        (TEXT, 'Text'),
        (RADIO, 'Radio'),
        (CHECKBOX, 'CheckBox')
]

QUESTION_NO = 0
QUESTION_MARKS = 0