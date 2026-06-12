from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile, Skill, Education, Experience, Project, Contact
from .forms import (LoginForm, RegistrationForm, ContactForm,
                    ProfileForm, SkillForm, EducationForm, ExperienceForm, ProjectForm)


# ─── Auth ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['username_or_email']
        password   = form.cleaned_data['password']
        # allow login with email
        if '@' in identifier:
            try:
                identifier = User.objects.get(email=identifier).username
            except User.DoesNotExist:
                pass
        user = authenticate(request, username=identifier, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'portfolio/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user, defaults={'full_name': user.username, 'email': user.email})
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    return render(request, 'portfolio/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Public Portfolio ─────────────────────────────────────────────────────────

def home(request):
    try:
        profile = Profile.objects.select_related('user').first()
    except Profile.DoesNotExist:
        profile = None
    projects = Project.objects.all()[:6] if profile else []
    skills   = Skill.objects.all()[:10]  if profile else []
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Message sent successfully!')
        return redirect('home')
    return render(request, 'portfolio/home.html', {
        'profile': profile, 'projects': projects,
        'skills': skills, 'contact_form': form,
    })


def about(request):
    profile   = Profile.objects.first()
    education = Education.objects.all()
    experience = Experience.objects.all()
    return render(request, 'portfolio/about.html', {
        'profile': profile, 'education': education, 'experience': experience,
    })


def projects_view(request):
    profile  = Profile.objects.first()
    projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'profile': profile, 'projects': projects})


def contact_view(request):
    profile = Profile.objects.first()
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'portfolio/contact.html', {'profile': profile, 'form': form})


def resume_view(request):
    profile    = Profile.objects.first()
    skills     = Skill.objects.all()
    education  = Education.objects.all()
    experience = Experience.objects.all()
    projects   = Project.objects.all()
    return render(request, 'portfolio/resume.html', {
        'profile': profile, 'skills': skills,
        'education': education, 'experience': experience, 'projects': projects,
    })


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username, 'email': request.user.email}
    )
    context = {
        'profile':    profile,
        'skills':     Skill.objects.filter(profile=profile),
        'education':  Education.objects.filter(profile=profile),
        'experience': Experience.objects.filter(profile=profile),
        'projects':   Project.objects.filter(profile=profile),
        'messages_count': Contact.objects.filter(is_read=False).count(),
    }
    return render(request, 'portfolio/dashboard.html', context)


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username}
    )
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated!')
        return redirect('dashboard')
    return render(request, 'portfolio/dashboard_form.html', {
        'form': form, 'title': 'Edit Profile'
    })


def _crud(request, Form, queryset_or_obj, title, redirect_to='dashboard'):
    """Generic add/edit helper."""
    instance = queryset_or_obj if hasattr(queryset_or_obj, 'pk') else None
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username}
    )
    form = Form(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        if not instance:
            obj.profile = profile
        obj.save()
        messages.success(request, f'{title} saved!')
        return redirect(redirect_to)
    return render(request, 'portfolio/dashboard_form.html', {'form': form, 'title': title})


@login_required
def add_skill(request):       return _crud(request, SkillForm, None, 'Add Skill')
@login_required
def edit_skill(request, pk):  return _crud(request, SkillForm, get_object_or_404(Skill, pk=pk), 'Edit Skill')
@login_required
def delete_skill(request, pk):
    get_object_or_404(Skill, pk=pk).delete()
    return redirect('dashboard')

@login_required
def add_education(request):       return _crud(request, EducationForm, None, 'Add Education')
@login_required
def edit_education(request, pk):  return _crud(request, EducationForm, get_object_or_404(Education, pk=pk), 'Edit Education')
@login_required
def delete_education(request, pk):
    get_object_or_404(Education, pk=pk).delete()
    return redirect('dashboard')

@login_required
def add_experience(request):       return _crud(request, ExperienceForm, None, 'Add Experience')
@login_required
def edit_experience(request, pk):  return _crud(request, ExperienceForm, get_object_or_404(Experience, pk=pk), 'Edit Experience')
@login_required
def delete_experience(request, pk):
    get_object_or_404(Experience, pk=pk).delete()
    return redirect('dashboard')

@login_required
def add_project(request):       return _crud(request, ProjectForm, None, 'Add Project')
@login_required
def edit_project(request, pk):  return _crud(request, ProjectForm, get_object_or_404(Project, pk=pk), 'Edit Project')
@login_required
def delete_project(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    return redirect('dashboard')

@login_required
def inbox(request):
    messages_list = Contact.objects.all()
    Contact.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'portfolio/inbox.html', {'messages_list': messages_list})
