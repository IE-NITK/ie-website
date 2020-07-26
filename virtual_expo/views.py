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
    return render(request,'navigation-using-RL.html')

def semantic_segmentation(request):
    return render(request,'semantic-segmentation.html')

def toll_cost_calculator(request):
    return render(request,'toll-cost-calculator.html')

def ndn(request):
    return render(request,'ndn.html')