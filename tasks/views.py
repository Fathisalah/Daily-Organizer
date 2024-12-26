from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Task, Category
from .forms import TaskForm, CategoryForm, CustomUserCreationForm
from django.utils import timezone
from django.contrib.auth import logout


# Add this new view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    # Get tasks for the current user
    tasks = Task.objects.filter(user=request.user)
    
    # Calculate statistics
    context = {
        'pending_tasks': tasks.filter(status='P').count(),
        'completed_tasks': tasks.filter(status='C').count(),
        'recent_tasks': tasks.order_by('-created_at')[:5],
        'categories': Category.objects.filter(user=request.user),
        'overdue_tasks': tasks.filter(due_date__lt=timezone.now(), status='P').count(),
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def task_list_view(request):
    # Get status filter from URL parameters
    status = request.GET.get('status')
    
    # Get base queryset for user's tasks
    tasks = Task.objects.filter(user=request.user)
    
    # Apply status filter if provided
    if status == 'P':
        tasks = tasks.filter(status='P')
    elif status == 'C':
        tasks = tasks.filter(status='C')
    
    # Order tasks by creation date
    tasks = tasks.order_by('-created_at')
    
    context = {
        'tasks': tasks,
        'current_status': status or 'all'
    }
    
    return render(request, 'task_list.html', context)

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')

@login_required
def task_complete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'C'
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, 'Task marked as complete!')
    return redirect('task_list')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})