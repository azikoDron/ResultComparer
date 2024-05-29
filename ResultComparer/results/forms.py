from django import forms



class DateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.initial['start_date'] = '2024-05-08'
        self.initial['start_time'] = '09:00'
        self.initial['end_date'] = '2024-05-08'
        self.initial['end_time'] = '18:00'
        self.initial['metric'] = 'pct95'

    start_date = forms.DateField(label="Start date", widget=forms.DateInput(attrs={"type": "date"}))
    start_time = forms.TimeField(label="", widget=forms.TimeInput(attrs={"type": "time", "value": "09:00"}))
    end_date = forms.DateField(label="End date", widget=forms.DateInput(attrs={"type": "date", "value": "2024-05-08"}))
    end_time = forms.TimeField(label="", widget=forms.TimeInput(attrs={"type": "time", "value": "18:00"}))
    metric = forms.ChoiceField(choices=(("pct95", "pct95"), ("pct99", "pct99")))




def time_post_form():
    pass