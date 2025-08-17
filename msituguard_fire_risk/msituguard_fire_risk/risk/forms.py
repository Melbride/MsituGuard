from django import forms

class CitizenReportForm(forms.Form):
    lat = forms.FloatField(widget=forms.HiddenInput())
    lon = forms.FloatField(widget=forms.HiddenInput())
    observation = forms.ChoiceField(choices=[
        ("smoke", "Smoke"),
        ("heat", "Heat"),
        ("flames", "Flames"),
        ("smell", "Burning smell"),
        ("other", "Other"),
    ])
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":3}))
