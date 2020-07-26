from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from virtual_expo import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'virtual_expo'

urlpatterns = [
    path('virtual-expo/', views.virtual_expo, name='virtual_expo'),
    path('virtual-expo/code/crowd-counting', views.crowd_counting, name='crowd-counting'),
    path('virtual-expo/code/indian-sign-lang-interpretor', views.indian_sign_lang_interpretor, name='indian-sign-lang-interpretor'),
    path('virtual-expo/code/image-captioning', views.image_captioning, name='image_captioning'),
    path('virtual-expo/code/mood_based_movie_recommender', views.mood_based_movie_recommender, name='mood_based_movie_recommender'),
    path('virtual-expo/code/navigation_using_RL', views.navigation_using_RL, name='navigation_using_RL'),
    path('virtual-expo/code/semantic_segmentation', views.semantic_segmentation, name='semantic_segmentation'),
    path('virtual-expo/code/toll_cost_calculator', views.toll_cost_calculator, name='toll_cost_calculator'),
    path('virtual-expo/code/ndn', views.ndn, name='NDN'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
