from django.urls import path

import blog.views as views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('write', views.PostCreate.as_view()),
    path('post/<slug>', views.PostDetails.as_view(), name='post-details'),
]
