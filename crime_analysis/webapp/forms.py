from django import forms

class UploadDatasetForm(forms.Form):
    file = forms.FileField(label='Select CSV or Parquet file')
