from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # Public
    path('',          views.home,          name='home'),
    path('about/',    views.about,         name='about'),
    path('projects/', views.projects_view, name='projects'),
    path('contact/',  views.contact_view,  name='contact'),
    path('resume/',   views.resume_view,   name='resume'),

    # Dashboard
    path('dashboard/',        views.dashboard,    name='dashboard'),
    path('dashboard/profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/inbox/',   views.inbox,        name='inbox'),

    # Skills CRUD
    path('dashboard/skills/add/',        views.add_skill,       name='add_skill'),
    path('dashboard/skills/<int:pk>/edit/',   views.edit_skill,  name='edit_skill'),
    path('dashboard/skills/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    # Education CRUD
    path('dashboard/education/add/',              views.add_education,    name='add_education'),
    path('dashboard/education/<int:pk>/edit/',    views.edit_education,   name='edit_education'),
    path('dashboard/education/<int:pk>/delete/',  views.delete_education, name='delete_education'),

    # Experience CRUD
    path('dashboard/experience/add/',             views.add_experience,   name='add_experience'),
    path('dashboard/experience/<int:pk>/edit/',   views.edit_experience,  name='edit_experience'),
    path('dashboard/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),

    # Projects CRUD
    path('dashboard/projects/add/',              views.add_project,    name='add_project'),
    path('dashboard/projects/<int:pk>/edit/',    views.edit_project,   name='edit_project'),
    path('dashboard/projects/<int:pk>/delete/',  views.delete_project, name='delete_project'),
]
