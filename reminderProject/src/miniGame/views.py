from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Plant, WaterTransaction

# Configuration
TOKENS_PER_DROP = 5  # 5 tokens = 1 water drop


@login_required
def game_home(request):
    """Main game view - display plant and game interface"""
    # Get or create plant for user
    plant, created = Plant.objects.get_or_create(user=request.user)
    
    # Calculate how many water drops user can buy
    user_tokens = request.user.tokens if hasattr(request.user, 'tokens') else 0
    max_drops_can_buy = user_tokens // TOKENS_PER_DROP
    
    # Calculate available drops (bought but not used)
    total_drops_bought = sum(t.water_drops_received for t in WaterTransaction.objects.filter(user=request.user))
    drops_used = plant.water_drops
    available_drops = total_drops_bought - drops_used
    
    context = {
        'plant': plant,
        'user_tokens': user_tokens,
        'tokens_per_drop': TOKENS_PER_DROP,
        'max_drops_can_buy': max_drops_can_buy,
        'stage_name': plant.get_stage_name(),
        'drops_needed': plant.drops_needed_for_next_stage(),
        'is_max_stage': plant.growth_stage >= 4,
        'available_drops': available_drops,
    }
    
    return render(request, 'miniGame/game.html', context)


@login_required
def buy_water(request):
    """Exchange tokens for water drops"""
    if request.method == 'POST':
        try:
            drops_to_buy = int(request.POST.get('drops', 1))
            
            if drops_to_buy < 1:
                messages.error(request, 'Invalid number of water drops!')
                return redirect('game_home')
            
            tokens_needed = drops_to_buy * TOKENS_PER_DROP
            user_tokens = request.user.tokens if hasattr(request.user, 'tokens') else 0
            
            # Check if user has enough tokens
            if user_tokens < tokens_needed:
                messages.error(request, f'Not enough tokens! You need {tokens_needed} tokens but only have {user_tokens}.')
                return redirect('game_home')
            
            # Use transaction to ensure atomicity
            with transaction.atomic():
                # Deduct tokens from user
                request.user.tokens -= tokens_needed
                request.user.save()
                
                # Record the transaction
                WaterTransaction.objects.create(
                    user=request.user,
                    tokens_spent=tokens_needed,
                    water_drops_received=drops_to_buy
                )
                
                messages.success(request, f'Successfully exchanged {tokens_needed} tokens for {drops_to_buy} water drop(s)! Click the plant to water it.')
            
            return redirect('game_home')
            
        except (ValueError, TypeError):
            messages.error(request, 'Invalid request!')
            return redirect('game_home')
    
    return redirect('game_home')


@login_required
def water_plant(request):
    """Water the plant with purchased drops"""
    if request.method == 'POST':
        try:
            # Get user's plant
            plant = Plant.objects.get(user=request.user)
            
            # Calculate available drops
            total_drops_bought = sum(t.water_drops_received for t in WaterTransaction.objects.filter(user=request.user))
            drops_used = plant.water_drops
            available_drops = total_drops_bought - drops_used
            
            if available_drops < 1:
                messages.error(request, 'You don\'t have any water drops! Buy some first.')
                return redirect('game_home')
            
            # Use one drop
            old_stage = plant.growth_stage
            plant.add_water_drop()
            new_stage = plant.growth_stage
            
            # Check if plant grew
            if new_stage > old_stage:
                messages.success(request, f'🌱 Amazing! Your plant grew to {plant.get_stage_name()}!')
            else:
                messages.success(request, f'💧 You watered your plant! Progress: {plant.water_progress}%')
            
            return redirect('game_home')
            
        except Plant.DoesNotExist:
            messages.error(request, 'Plant not found! Please try again.')
            return redirect('game_home')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid request!')
            return redirect('game_home')
    
    return redirect('game_home')


@login_required
def game_stats(request):
    """Display game statistics"""
    plant = Plant.objects.get_or_create(user=request.user)[0]
    transactions = WaterTransaction.objects.filter(user=request.user)
    
    total_tokens_spent = sum(t.tokens_spent for t in transactions)
    total_drops_bought = sum(t.water_drops_received for t in transactions)
    
    context = {
        'plant': plant,
        'total_tokens_spent': total_tokens_spent,
        'total_drops_bought': total_drops_bought,
        'total_transactions': transactions.count(),
        'recent_transactions': transactions[:10],
    }
    
    return render(request, 'miniGame/stats.html', context)
