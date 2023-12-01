from django.urls import path
from app.views import (
    home,
    login,
    signup,
    add_todo,
    signout,
    delete_todo,
    change_todo,
    all_tasks,
    specific_task,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup),
    path('add-todo/', add_todo),
    path('delete-todo/<int:id>/', delete_todo),
    path('change-status/<int:id>/<str:status>/', change_todo),
    path('logout/', signout),
    path('all-tasks/', all_tasks, name='all_tasks'),
    path('specific-task/<int:task_id>/', specific_task, name='specific_task'),
]
