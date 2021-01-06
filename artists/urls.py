from django.urls import path
from .views import (
    my_profile, 
    home_page, 
    edit_Profile,
    # ArtistProfileEdit, 
    SearchResultsItems, 
    CreateProfile, 
    view_profile, 
    ItemDashBoard, 
    DeleteItem, 
    EditItem,
    add_item_form,
    # AddItem,
    ItemView,
    load_cities,
)





urlpatterns = [
    path('', home_page, name = 'home_page'),
    path('search/', SearchResultsItems.as_view(), name = 'search_results'),
    path('my_profile/', my_profile, name = 'my_profile_page' ),
    path('my_dashboard/', ItemDashBoard.as_view(), name = 'my_dashboard' ),
    path('create_profile/', CreateProfile.as_view(), name = "create_profile"),
    path('edit_profile/<int:pk>', edit_Profile, name = 'edit_profile'),
    path('artist_profile/<int:pk>', view_profile, name = 'artist_profile_page'),
    path('item/<int:pk>', ItemView.as_view(), name = 'view_item'),
    path('delete_item/<int:pk>', DeleteItem.as_view(), name = 'delete_item'),
    path('edit_item/<int:pk>', EditItem.as_view(), name = 'edit_item'),
    path('add_item', add_item_form, name = 'add_item'),
    path('load_cities/', load_cities, name='load_cities'),
   
]

# path('load_cities/', load_cities, name='load_cities'), on django server a location we can call 