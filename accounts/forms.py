from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, models,  inlineformset_factory


from accounts.models import User,Skillset

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))



class EmployeeRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": "Enter First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": "Enter Last Name",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "Enter Email",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Confirm Password",
            }
        )

    class Meta:
        model = User
        
        exclude = ()
        fields = [
            "first_name",
            "last_name",
            'avatar',
            'gender',
            "resume",
            "email",
            "password1",
            "password2",
        ]
        error_messages = {
            "first_name": {
                "required": "First name is required",
                "max_length": "Name is too long",
            },
            "last_name": {
                "required": "Last name is required",
                "max_length": "Last Name is too long",
            },
            "gender": {"required": "Gender is required"},
        }

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user
    
class SkillsetForm(ModelForm):
    class Meta:
        model = Skillset
        fields = ['user','skill']
        exclude = ()
JobseekskilsFormset = inlineformset_factory(User, Skillset, form=SkillsetForm, extra=2)

class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["company_name"].label = "Company Name"
        self.fields["avatar"].label = "Company Logo"
        self.fields["address"].label = "Company Address"
        self.fields["registration_no"].label = "Company Registration Number"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["company_name"].widget.attrs.update(
            {
                "placeholder": "Enter Company Name",
            }
        )
        self.fields["address"].widget.attrs.update(
            {
                "placeholder": "Enter Company Address",
            }
        )
        
        self.fields["registration_no"].widget.attrs.update(
            {
                "placeholder": "Enter Company Reg No.",
            }
        )
        
        self.fields["telephone"].widget.attrs.update(
            {
                "placeholder": "Enter Company Phone No.",
            }
        )
        
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "Enter Email",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Confirm Password",
            }
        )
        
        

    class Meta:
        model = User
        fields = ["first_name", 
                  "last_name","registration_no",
                  "telephone",
                  "email",
                  "password1", 
                  "password2",
            ]
        error_messages = {
            "first_name": {
                "required": "First name is required",
                "max_length": "Name is too long",
            },
            "last_name": {
                "required": "Last name is required",
                "max_length": "Last Name is too long",
            },
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password"].widget.attrs.update({"placeholder": "Enter Password"})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": "Enter First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": "Enter Last Name",
            }
        )    
        self.fields["avatar"].widget.attrs.update(
            {
                "placeholder": "Profile Picture",
            }
        )
        
        self.fields["telephone"].widget.attrs.update(
            {
                "placeholder": "Telephone Number",
            }
        )

    class Meta:
        model = User #user
        fields = ["avatar","first_name", "last_name", "resume", "email","telephone","working_experience","birth_date","address"]

class ResetEmailForm(forms.Form):
    email = forms.EmailField()
    
class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())