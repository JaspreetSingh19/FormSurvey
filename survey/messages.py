"""
This file defines dictionaries containing validation error messages and success messages
for the survey app.
The VALIDATION dictionary contains error messages for form validation,
while the SUCCESS_MESSAGES dictionary contains success messages for various operations in the app.
"""
VALIDATION = {
    'form_name': {
        "blank": "Form name can not be blank",
        "required": "Please provide a form name",
        "exists": "Form with this name already exists"
    },
    'description': {
        "blank": "Form Description can not be blank",
        "required": "Please provide a form description",

    },
    'forms': {
        'no_forms': 'No forms found',
        'no_forms_assigned': 'No forms assigned'
    },
    'block_name': {
        "blank": "Block name can not be blank",
        "required": "Please provide a block name",
        "exists": "Block with this name already exists"
    },
    'survey_id': {
        "required": "Please provide a survey form id",
    },
    'blocks': {
        "no_blocks": " No blocks found"
    },
    'question': {
        "required": "Please provide question",
        "no_questions": " No questions found",
    },
    'default_question': {
        "no_questions": " No questions found",
    },
    'question_no': {
        "required": "Please provide question number",
        "valid": "Question number cannot be less or equal to 0",
        "exists": "Question number already exists",

    },
    'type': {
        'required': 'PLease select the question type'
    },
    'block_id': {
        "required": "Please provide a block id",
    },
    'marks': {
        "required": "Please provide marks for questions ",
        "valid": "Question marks cannot be less or equal to 0",
    },
    'choice': {
        "required": "Please provide choice for questions ",
        'no_choices': 'No Options found'
    },
    'question_id': {
        "required": "Please provide question id ",
    },
    'choice_no': {
        "required": "Please provide choice no ",
        "valid": "Choice Number cannot be less or equal to 0",
        "exists": "Choice number already exists",

    },
    'text': {
        'one_choice': 'Text question can have only one choice'
    },
    'correct': {
        'exists': 'Radio cannot have more than one correct option .Please choose another option'
    },
    'is_published': {
        'False': 'Survey cannot be published until it has at least one block with at least one question.'
    },
    'name': {
        'required': 'PLease provide a name'
    },
    'blocks_or_questions': {
        'not_found': 'No blocks or questions found. '
                     'Survey cannot be published until it has at least one block with at least one question.'
    },

}
SUCCESS_MESSAGES = {
    "FORM": {
        "CREATED_SUCCESSFULLY": "Form created successfully",
        "UPDATED_SUCCESSFULLY": "Form updated successfully",
        "DELETED_SUCCESSFULLY": "Form deleted successfully",
        "SUBMITTED_SUCCESSFULLY": "Form submitted successfully",
        "PUBLISHED_SUCCESSFULLY": "Form published successfully",
        "ASSIGNED_SUCCESSFULLY": "Form assigned successfully "

    },
    "BLOCK": {
        "CREATED_SUCCESSFULLY": "Block created successfully",
        "UPDATED_SUCCESSFULLY": "Block updated successfully",
        "DELETED_SUCCESSFULLY": "Block deleted successfully",
    },
    "QUESTION": {
        "CREATED_SUCCESSFULLY": "Question created successfully",
        "UPDATED_SUCCESSFULLY": "Question updated successfully",
        "DELETED_SUCCESSFULLY": "Question deleted successfully",
    },
    "QUESTION_CHOICE": {
        "CREATED_SUCCESSFULLY": "Question Option created successfully",
        "UPDATED_SUCCESSFULLY": "Question Option updated successfully",
        "DELETED_SUCCESSFULLY": "Question Option deleted successfully",
    },
}
ERROR_MESSAGES = {
    "FORM": {
        "SAVED_AS_DRAFT": "Form cannot be published until there is one block with a question,"
                          " Form saved as Draft",
    }
}
