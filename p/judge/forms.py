from django import forms

class SubmissionForm(forms.Form):
  method = forms.ChoiceField(
    widget=forms.RadioSelect,
    choices=(
      ('textarea', 'Past code here'),
      ('file', 'Upload source file')
    )
  )
  code_text = forms.CharField(
    widget=forms.Textarea
  )
  code_file = forms.FileField()
  problem_id = forms.IntegerField(
    widget=forms.HiddenInput
  )

