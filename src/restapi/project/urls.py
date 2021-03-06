from django.urls import path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from ..project import views as views

urlpatterns = [
    path('', views.ProjectView.as_view(), name='api-add-project'),
    path('issue', views.IssueView.as_view(), name='api-add-issue'),
    path('issue/reply', views.IssueReplyView.as_view(), name='api-add-issue-reply'),
    path('issue/comment', views.IssueCommentView.as_view(), name='api-add-issue-comment')
]
