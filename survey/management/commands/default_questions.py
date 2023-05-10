"""
This file defines custom commands to generate default questions
for 'DefaultQuestion' model
"""
from django.core.management.base import BaseCommand
from survey.models import DefaultQuestion

text_question = {
    "label": "Please enter your answer:",
    "required": True
}

radio_question = {
    "label": "Select the correct answer:",
    "choices": [
        {"label": "Option 1", "value": "1", "marks": "0"},
        {"label": "Option 2", "value": "2", "marks": "0"},
        {"label": "Option 3", "value": "3", "marks": "0"},
    ],
    "required": True
}

checkbox_question = {
    "label": "Select all that apply:",
    "choices": [
        {"label": "Option 1", "value": "1", "marks": "0"},
        {"label": "Option 2", "value": "2", "marks": "0"},
        {"label": "Option 3", "value": "3", "marks": "0"},
    ],
    "required": True
}


class Command(BaseCommand):
    help = 'Create default questions'

    def handle(self, *args, **options):
        # Create text question
        text = DefaultQuestion.objects.create(
            name='Text Question',
            question_type='text',
            properties=text_question,
            marks=1.0
        )

        # Create radio question
        radio = DefaultQuestion.objects.create(
            name='Radio Question',
            question_type='radio',
            properties=radio_question,
            marks=2.0
        )

        # Create checkbox question
        checkbox = DefaultQuestion.objects.create(
            name='Checkbox Question',
            question_type='checkbox',
            properties=checkbox_question,
            marks=3.0
        )

        self.stdout.write(self.style.SUCCESS('Default questions created'))
