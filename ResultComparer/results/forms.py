from django import forms


class DateForm(forms.Form):
    start_date = forms.DateTimeInput()
    start_date = forms.DateTimeField(label="Start date")
    end_time = forms.DateTimeField()





def time_post_form():
    pass