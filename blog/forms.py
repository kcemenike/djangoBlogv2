from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "id":"form_full_name",
                "placeholder":"Your full name",
                }))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class":"form-control",
                "id":"form_email",
                "placeholder":"Your email address",
                }))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "placeholder":"Your message",
            }))

    # Create validation for email (let's assume it must be gmail.com)
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={}))

class RegisterForm(forms.Form):
    username = forms.CharField()
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Confirm password", widget=forms.PasswordInput)

    # Create validation for password (they must both match)
    # In summary, it cleans the data, does the validation, then returns the same data
    def clean(self):
        data = self.cleaned_data

        # Validate password matching
        password = self.cleaned_data['password']
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match")
        
        # Validate username is not yet taken
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is taken")

        # Make sure email is not yet taken
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is taken")

        return data

    # Make sure username is not taken by validating
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     # Check to see if the username exists
    #     qs = User.objects.filter(username=username)
    #     if qs.exists():
    #         raise forms.ValidationError("Username is taken")
    #     return username
    #     # we can also add this to the def clean(self)