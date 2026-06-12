from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Education, Experience, Project, Contact


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in
                   ['full_name', 'title', 'phone', 'email', 'address', 'linkedin', 'github', 'website']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['profile']
        widgets = {
            'name':       forms.TextInput(attrs={'class': 'form-control'}),
            'level':      forms.Select(attrs={'class': 'form-select'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['profile']
        widgets = {
            'institution':    forms.TextInput(attrs={'class': 'form-control'}),
            'degree':         forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'start_year':     forms.NumberInput(attrs={'class': 'form-control'}),
            'end_year':       forms.NumberInput(attrs={'class': 'form-control'}),
            'description':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'currently_studying': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['profile']
        widgets = {
            'company':          forms.TextInput(attrs={'class': 'form-control'}),
            'position':         forms.TextInput(attrs={'class': 'form-control'}),
            'start_date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date':         forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location':         forms.TextInput(attrs={'class': 'form-control'}),
            'currently_working': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['profile']
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            'project_url':  forms.URLInput(attrs={'class': 'form-control'}),
            'github_url':   forms.URLInput(attrs={'class': 'form-control'}),
            'image':        forms.FileInput(attrs={'class': 'form-control'}),
        }
