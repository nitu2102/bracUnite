from django import forms
from .models import Profile, GENDER_CHOICES, BLOOD_GROUP_CHOICES

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'name', 'profile_pic', 'hobby', 'department', 'blood_group', 'gender',
                  'role', 'room_no', 'research_interest', 'current_city']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=GENDER_CHOICES),
            'blood_group': forms.Select(choices=BLOOD_GROUP_CHOICES),
            'profile_pic': forms.FileInput(attrs={'accept': 'image/*'}),
        }