from django.shortcuts import render

# Create your views here.


def virtual_expo(request):
    return render(request, 'virtual_expo.html')


def crowd_counting(request):
    return render(request, 'crowd_counting.html')


def indian_sign_lang_interpretor(request):
    return render(request, 'indian-sign-lang-interpretor.html')


def image_captioning(request):
    return render(request, 'image-captioning.html')


def mood_based_movie_recommender(request):
    return render(request, 'mood-based-movie-recommender.html')


def navigation_using_RL(request):
    return render(request, 'navigation-using-RL.html')


def semantic_segmentation(request):
    return render(request, 'semantic-segmentation.html')


def toll_cost_calculator(request):
    return render(request, 'toll-cost-calculator.html')


def ndn(request):
    return render(request, 'ndn.html')


def autonomous_driving_car(request):
    return render(request, 'autonomous-driving-car.html')


def child_safety(request):
    return render(request, 'child-safety.html')


def human_activity_recognition(request):
    return render(request, 'human-activity-recognition.html')


def ocr(request):
    return render(request, 'ocr.html')


def skinput_based_robot(request):
    return render(request, 'skinput-based-robot.html')


def smart_home_automation(request):
    return render(request, 'smart-home-automation.html')


def traffic_light_control(request):
    return render(request, 'traffic-light-control.html')


def uart_on_fpga(request):
    return render(request, 'uart-on-fpga.html')


def autoshopper(request):
    return render(request, 'autoshopper.html')


def robotic_arm(request):
    return render(request, 'robotic-arm.html')


def terrain_mapping(request):
    return render(request, 'terrain-mapping.html')


def drag_system(request):
    return render(request, 'drag-system.html')


def exhaust_duct(request):
    return render(request, 'exhaust-duct.html')


def town_planning(request):
    return render(request, 'town-planning.html')
