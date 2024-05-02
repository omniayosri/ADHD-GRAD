from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.user_register_view, name="register"),
    path("list-patients/", views.ListPatients.as_view(), name="register"),
    path("create/task/", views.ListCreateTaskView.as_view(), name="create_task"),
    path("list/task/", views.ListCreateTaskView.as_view(), name="list_task"),
    path(
        "update/task/<int:pk>/",
        views.UpdateDeleteRetrieveTaskView.as_view(),
        name="update_task",
    ),
    path(
        "delete/task/<int:pk>/",
        views.UpdateDeleteRetrieveTaskView.as_view(),
        name="delete_task",
    ),
    path(
        "retrieve/task/<int:pk>/",
        views.UpdateDeleteRetrieveTaskView.as_view(),
        name="retrieve_task",
    ),
    path("search/task/", views.SearchListView.as_view(), name="search_task"),

    path("fav/task/", views.FavoritesListView.as_view(), name='fav_task'),
    path("trash/task/", views.TrashListView.as_view(), name='trash_task'),
    path("hidden/task/", views.HiddenListView.as_view(), name='hidden_task'),
    path("list-appointment/", views.ListAppointments.as_view(), name='list_appointments'),
]
