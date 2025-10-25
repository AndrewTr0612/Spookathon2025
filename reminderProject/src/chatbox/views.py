from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
import random
from datetime import datetime

# Mental support content for Spooky Buddie
STRESS_ACTIVITIES = [
    "🧘‍♀️ Try a 5-minute meditation session to calm your mind",
    "🚶‍♂️ Take a short walk outside to refresh yourself",
    "🎵 Listen to your favorite calming music for 10 minutes",
    "💭 Practice deep breathing: breathe in for 4, hold for 4, out for 4",
    "📝 Write down 3 things you're grateful for today",
    "🌿 Do some light stretching or yoga poses",
    "☕ Make yourself a cup of tea and enjoy it mindfully",
    "🎨 Doodle or color for a few minutes to relax",
    "📱 Call or text a friend to share how you're feeling",
    "🛁 Take a warm shower or bath to unwind",
]

BREAK_SUGGESTIONS = [
    "⏰ It's time for a 5-minute break! Stand up and stretch.",
    "🌟 Take a 10-minute break to recharge your energy.",
    "💧 Break time! Hydrate yourself with a glass of water.",
    "👀 Give your eyes a rest - look at something 20 feet away for 20 seconds.",
    "🍎 Snack break! Grab a healthy treat to fuel your body.",
    "🌬️ Step outside for some fresh air for 5 minutes.",
    "⏸️ Pause and take 3 deep breaths. You deserve this break!",
    "🎯 Take a 15-minute break to avoid burnout. You're doing great!",
]

INSPIRING_QUOTES = [
    "💪 'You are stronger than you think. Keep going!'",
    "🌟 'Every accomplishment starts with the decision to try.'",
    "🌈 'Believe in yourself and all that you are.'",
    "✨ 'Progress, not perfection. You're doing amazing!'",
    "🎯 'Small steps every day lead to big changes.'",
    "🌸 'Be kind to yourself. You're doing the best you can.'",
    "🚀 'Your potential is endless. Don't stop believing!'",
    "🌻 'Tough times don't last, but tough people do.'",
    "💫 'You are capable of amazing things!'",
    "🦋 'Growth happens outside your comfort zone.'",
    "☀️ 'Today is a new opportunity to be your best self.'",
    "🌙 'Rest when you need to. Self-care isn't selfish.'",
    "🎈 'You are enough, just as you are.'",
    "🌺 'Embrace the journey, not just the destination.'",
    "⭐ 'Your mindset determines your success. Think positive!'",
]

def get_ai_response(user_message, user):
    """Generate response based on user message keywords"""
    message_lower = user_message.lower()
    
    # Get user's display name safely
    user_name = user.first_name if user.first_name else user.username
    
    # Check for stress-related keywords
    if any(word in message_lower for word in ['stress', 'stressed', 'anxious', 'anxiety', 'overwhelm', 'tired', 'exhausted']):
        return """Here are some stress-relief suggestions:

🧘‍♀️ Try a 5-minute meditation session
🚶‍♂️ Take a short walk outside
💭 Practice deep breathing exercises
📝 Write down 3 things you're grateful for
🌿 Do some light stretching or yoga
☕ Make yourself a cup of tea
🎨 Doodle or color for a few minutes
� Call a friend to talk

Remember, taking care of yourself is important!"""
    
    # Check for break-related keywords
    elif any(word in message_lower for word in ['break', 'rest', 'pause', 'working']):
        return """Time to take a break! Here are some suggestions:

⏰ Take a 5-minute break and stretch
💧 Drink a glass of water
👀 Look away from screen - rest your eyes
🍎 Grab a healthy snack
🌬️ Step outside for fresh air
⏸️ Take 3 deep breaths

Taking breaks is essential for productivity!"""
    
    # Check for motivation/quote keywords
    elif any(word in message_lower for word in ['motivate', 'inspire', 'quote', 'encourage', 'support', 'help', 'sad', 'down']):
        quotes = [
            "💪 You are stronger than you think. Keep going!",
            "🌟 Every accomplishment starts with the decision to try.",
            "✨ Progress, not perfection. You're doing amazing!",
            "🎯 Small steps every day lead to big changes.",
            "🌸 Be kind to yourself. You're doing the best you can.",
        ]
        selected_quote = random.choice(quotes)
        return f"""Here's some motivation for you:

{selected_quote}

You're doing great! Keep being awesome!"""
    
    # Check for activity suggestions
    elif any(word in message_lower for word in ['activity', 'activities', 'what can i do', 'suggestions', 'suggest']):
        return """Here are some activities you can try:

🧘‍♀️ Meditation or mindfulness
🚶‍♂️ Walking or light exercise
🎵 Listen to calming music
📝 Journaling your thoughts
🌿 Stretching or yoga
🎨 Creative activities (drawing, coloring)
📱 Connect with friends or family
� Take a relaxing bath

Pick one that feels right for you!"""
    
    # Greeting responses
    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon']):
        return f"""Hey there, {user_name}! 👋

I'm Spooky Buddie, your wellness companion. I can help you with:

• Stress-reducing activities
• Break time suggestions
• Inspiring quotes and motivation
• Activity recommendations

Just type what you need help with!"""
    
    # Help command
    elif any(word in message_lower for word in ['help', '?', 'what can you do']):
        return f"""Hi {user_name}! Here's what I can help you with:

🧘 **Stress Relief**: Tell me you're stressed
⏰ **Break Reminders**: Ask for a break
💪 **Motivation**: Ask for inspiration
🎯 **Activities**: Ask for activity suggestions

Try saying:
• "I'm feeling stressed"
• "I need a break"
• "Give me motivation"
• "Suggest an activity"

What would you like help with?"""
    
    # Default response
    else:
        return f"""Hi {user_name}! I'm here to help you with wellness support.

Try asking me about:
• Stress relief activities
• Taking a break
• Motivational quotes
• Activity suggestions

What do you need today?"""

@login_required
def chat_view(request):
    """Main chat interface"""
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        print(f"DEBUG: Received POST request")
        print(f"DEBUG: User message: '{user_message}'")
        print(f"DEBUG: Is AJAX: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")
        
        if user_message:
            try:
                # Generate AI response
                ai_response = get_ai_response(user_message, request.user)
                print(f"DEBUG: Generated response: {ai_response[:50]}...")
                
                # Save chat message
                chat_msg = ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=ai_response
                )
                print(f"DEBUG: Saved to database with ID: {chat_msg.id}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'message': user_message,
                        'response': ai_response,
                        'timestamp': datetime.now().strftime('%I:%M %p')
                    })
                
                return redirect('chat')
            except Exception as e:
                # Handle errors gracefully
                print(f"ERROR in chat_view: {e}")
                import traceback
                traceback.print_exc()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'Sorry, something went wrong. Please try again.'
                    }, status=500)
                return redirect('chat')
        else:
            print(f"DEBUG: Empty message received")
    
    # Get recent chat history
    recent_chats = ChatMessage.objects.filter(user=request.user)[:20]
    
    return render(request, 'chatbox/chat.html', {
        'recent_chats': reversed(list(recent_chats))
    })

@login_required
def clear_chat(request):
    """Clear chat history"""
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
    return redirect('chat')
