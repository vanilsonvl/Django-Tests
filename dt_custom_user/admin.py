#coding: utf-8

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from dt_custom_user.models import CustomUser

# Register your models here.

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
	fields = ('name', 'email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
	password2 = self.cleaned_data.get('password2')
	
	if password1 and password2 and password1 != password2:
	    raise forms.ValidationError('Passwords dont match')

	return password2

    def save(self, commit=True):
	user = super(UserCreationForm, self).save(commit=False)
	user.set_password(self.cleaned_data['password1'])

	if commit:
	    user.save()
	return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
	model = CustomUser
	fields = ('name', 'email', 'password', 'is_active', 'is_admin', 'is_staff')

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(BaseUserAdmin):
   
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'is_staff', 'is_admin', 'is_active')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'is_active')}),
        ('Admin Infos', {'fields': ('is_admin', 'is_staff', )}),
    )
    add_fieldsets = (
	(None, {
	    'classes': ('wide',),
	    'fields': ('name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('name', 'email',)
    ordering = ('-is_staff', '-is_admin', '-is_active', 'name')
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
