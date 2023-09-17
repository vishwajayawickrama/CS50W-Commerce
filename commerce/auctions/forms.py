from django import forms


class CreateListForm(forms.Form):
    title = forms.CharField(label="Title :", max_length=100)
    description = forms.CharField(label="Description :", max_length=1000)
    imageUrl = forms.CharField(label="Image Link :", required=False)
    price = forms.IntegerField(label="Starting Price :")
    
    
class CreateComments(forms.Form):
    comment = forms.CharField(label="Enter Your Comment  ", max_length=1000)