import os
import google.generativeai as genai
from django.http import HttpResponse
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.http import HttpResponse

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer



load_dotenv()


# Ensure this is correctly set up
bot = ChatBot('chatbot', read_only=False, logic_adapters=[{
    'import_path': 'chatterbot.logic.BestMatch',
    'default_response': 'Sorry, I dont know what that means',  # Added comma
    'maximum_similarity_threshold': 0.90
}])

 
list_to_train = [
    "hi",
    "Hello! Ready to crush your workout today?",
    "what's your name?",
    "I'm just a fitness chatbot named Inshape here to motivate you!",
    "how can I get fit?",
    "Start with a balanced diet and regular exercise.",
    "what should I eat before a workout?",
    "A mix of carbs and protein is ideal. Try a banana with peanut butter!",
    "how do I stay motivated?",
    "Set clear goals and track your progress. Remember, consistency is key!",
    "I need a workout plan.",
    "What are your fitness goals? Weight loss, muscle gain, or general fitness?",
    "how often should I train?",
    "Aim for at least 3-5 times a week for optimal results.",
    "what's a good warm-up?",
    "Dynamic stretches and light cardio are great for warming up.",
    "I don't feel like working out.",
    "Remember why you started! A little workout is better than none.",
    "what exercises should I do for abs?",
    "Try planks, crunches, and leg raises for a great core workout.",
    "how do I build muscle?",
    "Focus on strength training with compound exercises like squats and deadlifts.",
    "I want to lose weight.",
    "Combine a healthy diet with regular exercise for the best results.",
    "can you give me a motivational quote?",
    "Sure! 'The only bad workout is the one that didn’t happen.'",
    "what should I do after my workout?",
    "Cool down with stretches and hydrate to help your recovery.",
    "I want to join a gym.",
    "Look for one with good equipment and classes that interest you!",
    
    # AI-driven enhancements
    "can you suggest a workout based on my goals?",
    "Sure! Tell me your goals: weight loss, muscle gain, or endurance.",
    "how can I track my progress?",
    "You can log your workouts and meals in the app to see your progress over time.",
    "what should my meal plan look like?",
    "It should include a balance of proteins, carbs, and healthy fats tailored to your goals.",
    "I need help with my nutrition.",
    "Let’s assess your current diet and suggest some improvements.",
    "how do I maintain consistency?",
    "Set a schedule, track your workouts, and find an accountability partner!",
    "give me a tip for better exercise form.",
    "Focus on your posture and control your movements. Quality over quantity!",
    "how does AI personalize my experience?",
    "AI analyzes your activity and preferences to tailor workouts and nutrition plans just for you.",
    "what insights can I gain from my behavior?",
    "AI identifies patterns in your activity, helping you understand what keeps you engaged.",
    "can I ask for a specific type of workout?",
    "Absolutely! Just tell me the type you prefer, like HIIT or strength training.",
    "how do I prevent injuries?",
    "Always warm up properly, listen to your body, and don't push through pain.",
]




list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about-us.html')

def classes(request):
    return render(request, 'class-details.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

def class_timetable(request):
    return render(request, 'class-timetable.html')

def bmi_calculator(request):
    return render(request, 'bmi-calculator.html')

def gallery(request):
    return render(request, 'gallery.html')

def blog(request):
    return render(request, 'blog.html')

def error_404(request):
    return render(request, '404.html')

def contact(request):
    return render(request, 'contact.html')



def profile(request):
    return render(request, 'profile.html')


def getResponse(request):
    userMessage = request.GET.get('userMessage')
    chatResponse = str(bot.get_response(userMessage))
    
    # Check if ChatterBot's default response was returned
    if chatResponse == 'Sorry, I dont know what that means':
        # Define a Gemini prompt for unknown questions
        prompt = f"Answer this question as a fitness chatbot: {userMessage}"

        # Configure the generation settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 512
        }

        # Start a chat session and query Gemini API
        model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)
        chat_session = model.start_chat()
        response = chat_session.send_message(prompt)

        # Use the Gemini response if it exists
        if response and response.text:
            chatResponse = response.text
        else:
            chatResponse = "Sorry, I'm unable to assist with that question at the moment."

    return HttpResponse(chatResponse)