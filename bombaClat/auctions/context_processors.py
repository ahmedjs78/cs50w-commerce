from .models import User,Listings, Category,Bid



def add_variable_to_context(request):
    all_catagores = Category.objects.all()
    return {
        'testme': 'Hello world!','all_catagores':all_catagores
    }