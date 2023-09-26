from .models import *
from django import forms



class MomForm (forms.ModelForm):
    class Meta:
        model = MomModel
        fields = '__all__'
        exclude = ['user','email']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name','description']
        exclude = ['moms']

class MenuItemForm(forms.ModelForm):
    menu = forms.ModelChoiceField(queryset=Menu.objects.all())

    class Meta:
        model = MenuItem
        fields = ['menu','name','price','item_image','description','is_available']
    # show related option that only the autheticated user can modify their own data in relationship cannot view other related data 
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['menu'].queryset = Menu.objects.filter(moms__user = user)

