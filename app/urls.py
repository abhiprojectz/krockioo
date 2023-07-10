from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.autodiscover()
admin.site.login = login_required(admin.site.login)


app_name = 'app'


urlpatterns = [
    re_path(r'^dashboard/(?P<id>[a-zA-Z0-9]{10})/$', views.Dashboard.as_view(), name='dashboard'),


    path('api/download', views.DownloadPDF.as_view(), name="download"),

    path('projects', views.AppPanel.as_view(), name="app_panel"),
    path('api/generate_text', views.GenerateTextView.as_view(), name="generate_text"),
    path('api/generate_suggestion', views.GenerateSuggestion.as_view(), name="generate_suggestion"),

    path('api/generate_image', views.GenerateImage.as_view(), name="generate_image"),
    path('api/generate_all_images', views.GenerateAllImages.as_view(), name="generate_all_images"),
    path('api/update_text', views.UpdateText.as_view(), name="update_text"),


    path('api/create_board', views.CreateBoard.as_view(), name="create_board"),
    path('api/create_board_slide', views.CreateBoardSlide.as_view(), name="create_board_slide"),



    path('api/get_all_boards', views.GetAllBoards.as_view(), name="get_all_boards"),
    path('api/get_all_slides', views.GetAllSlides.as_view(), name="get_all_slides"),



    path('api/delete_board', views.DeleteBoard.as_view(), name="delete_board"),
    path('api/delete_slide', views.DeleteSlide.as_view(), name="delete_slide"),


    path('api/delete_all_slides', views.DeleteAllSlides.as_view(), name="delete_all_slides"),
    path('api/delete_all_boards', views.DeleteAllBoards.as_view(), name="delete_all_boards"),

    path('api/update_board', views.UpdateBoard.as_view(), name="update_board"),
    path('api/update_board_slide', views.UpdateBoardSlide.as_view(), name="update_board_slide"),

    # path('api/generate_text', views.GenerateTextView.as_view(), name="generate_text"),
    # path('api/generate_text', views.GenerateTextView.as_view(), name="generate_text"),
    # path('api/generate_text', views.GenerateTextView.as_view(), name="generate_text"),


    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
]