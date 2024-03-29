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
            "first_name", "last_name", 'avatar', 'gender',
            'birth_date', 'telephone','residence', "resume",
            'academic_qualification','job_preference',   'level',  'profile_summary',   'current_salary',
            'expected_salary',"email", "password1",  "password2", "terms_and_conditions",
            
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
    class Meta:
        model = User
        fields = ["company_name", "avatar", "registration_no",
                  "reg_document", 'address',  "telephone","industry",
                  "email",   "password1",   "password2",
            ]
        error_messages = {
            "company": {
                "required": "Company name is required",
                "max_length": "Name is too long",
            },
            "avatar": {
                "required": "Company logo is required",
                "max_length": "Company Logo is too big",
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

class EmployerProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployerProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["reg_document"].label = "Registration Certificate"
        self.fields["avatar"].label = "Company Logo"
        
        self.fields["company_website_url"].label = "Company Website e.g https://your_company.com"

    class Meta:
        model = User #user model
        fields = ["avatar","company_name","industry", "registration_no", "reg_document", "email","telephone","address","profile_summary",'company_website_url']

class EmployeeProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User #user model
        fields = [  "first_name","last_name",'avatar', 'gender',  'birth_date', 'telephone',   'residence',  "resume", 'academic_qualification', 'job_preference',  'level',  'profile_summary',   'current_salary',  'expected_salary',   "email",  "terms_and_conditions",'working_experience']

class ResetEmailForm(forms.Form):
    email = forms.EmailField()
    
class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())