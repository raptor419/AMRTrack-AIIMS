from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap_datepicker_plus import DatePickerInput
from app.variables import *


class InputForm2(forms.Form):
    ams2 = forms.ChoiceField(widget=forms.RadioSelect, label="Select Antimicrobial", required=True,
                             choices=[(x, x) for x in ANTIMICROBIALS])

    def __init__(self, *args, **kwargs):
        super(InputForm2, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Generate Plot', css_class='btn btn-success'))
        self.helper.form_method = 'POST'


class InputDataForm(forms.Form):
    keywords = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Keywords'}), required=False)
    ams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(x, x) for x in ANTIMICROBIALS],
                                    label="Select Antimicrobial", required=False)
    site = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(x, x) for x in SITES],
                                     label="Select Collection Location", required=False)
    org = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(x, x) for x in ORGANISMS],
                                    label="Select Organisms", required=False)
    col = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(x, x) for x in COLLTYPES],
                                    label="Select Collection Type", required=False)
    hosp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(x, x) for x in HOSPTIALS],
                                     label="Select Hospitals", required=False)
    startdate = forms.DateField(label='Enter End Date', widget=DatePickerInput, required=False)
    enddate = forms.DateField(label='Enter Start Date', widget=DatePickerInput, required=False)

    def __init__(self, *args, **kwargs):
        super(InputDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Generate Sensitivity Table', css_class='btn btn-success'))
        self.helper.form_method = 'POST'
