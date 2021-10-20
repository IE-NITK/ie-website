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
    path('virtual-expo/gadget/autonomous_driving_car', views.autonomous_driving_car, name='autonomous_driving_car'),
    path('virtual-expo/gadget/child_safety', views.child_safety, name='child_safety'),
    path('virtual-expo/gadget/human_activity_recognition', views.human_activity_recognition, name='human_activity_recognition'),
    path('virtual-expo/gadget/ocr', views.ocr, name='OCR'),
    path('virtual-expo/gadget/skinput_based_robot', views.skinput_based_robot, name='skinput_based_robot'),
    path('virtual-expo/gadget/smart_home_automation', views.smart_home_automation, name='smart_home_automation'),
    path('virtual-expo/gadget/traffic_light_control', views.traffic_light_control, name='traffic_light_control'),
    path('virtual-expo/gadget/uart_on_fpga', views.uart_on_fpga, name='uart_on_fpga'),
    path('virtual-expo/robotics/autoshopper', views.autoshopper, name='autoshopper'),
    path('virtual-expo/robotics/robotic_arm', views.robotic_arm, name='robotic_arm'),
    path('virtual-expo/robotics/terrain_mapping', views.terrain_mapping, name='terrain_mapping'),
    path('virtual-expo/garage/exhaust_duct', views.exhaust_duct, name='exhaust_duct'),
    path('virtual-expo/garage/town_planning', views.town_planning, name='town_planning'),
    path('virtual-expo/garage/drag_system', views.drag_system, name='drag_system'),
    path('virtual-expo/garage/material_synthesis', views.material_synthesis, name='material_synthesis'),
    path('virtual-expo/capital/opec', views.opec, name='opec'),
    path('virtual-expo/capital/risk_assessment', views.risk_assesment, name='risk_assessment'),
    path('virtual-expo/capital/app_based_delivery', views.app_based_delivery, name='app_based_delivery'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
