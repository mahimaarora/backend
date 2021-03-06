import uuid
from djoser.views import UserView, UserDeleteView
from djoser import serializers
from rest_framework import views, permissions, status, permissions, generics, filters
from rest_framework.response import Response
from . import models, serializers, constants
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


class ProjectView(views.APIView):
    """Use this endpoint to add projects in the backend."""

    def get(self, request):
        queryset = models.Project.objects.all()
        project_id = self.request.query_params.get('id', None)

        if project_id is None:
            response = []
            for project in list(queryset):
                response.append(project.to_dict())
            return Response(response)
        else:
            try:
                project = models.Project.objects.get(project_id=project_id)
            except:
                return Response([])
            project_issues = models.Issue.objects.filter(project_id=project.id)
            checkpoint_data = {}
            for name in constants.CHECKPOINT_NAMES:
                checkpoint_data[name] = []

            for issue in project_issues:
                try:
                    if issue.id not in checkpoint_data[issue.checkpoint_name]:
                        checkpoint_data[issue.checkpoint_name].append(issue.id)
                except:
                    pass
            project.area_of_issues_open.append(checkpoint_data)
            return Response(project.to_dict())

    def post(self, request):
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_reference = self.request.data['update_reference']
        project_id = self.request.data['project_id']
        new_value = self.request.data['new_value']

        project = models.Project.objects.get(project_id=project_id)

        serializer = serializers.ProjectSerializer(
            project, data={update_reference: new_value}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ProjectSerializer


class IssueView(views.APIView):
    """Use this endpoint to add projects in the backend."""

    def get(self, request):
        queryset = models.Issue.objects.all()
        issue_ids = self.request.query_params.get('id', None)

        if issue_ids is None:
            response = []
            for issue in list(queryset):
                response.append(issue.to_dict())
            return Response(response)
        else:
            issue_list = []
            for issue_id in issue_ids.split(',')[:-1]:
                try:
                    issue = models.Issue.objects.get(pk=issue_id)
                except:
                    return []
                comments = issue.issuecomment_set.filter(issue_id=issue_id)
                for comment in comments:
                    replies = comment.issuereply_set.filter(
                        comment_id=comment.id)
                    for reply in replies:
                        comment.comment_replies.append(reply.to_dict())
                    issue.comments.append(comment.to_dict())
                issue_list.append(issue.to_dict())

            return Response(issue_list)

    def post(self, request):
        serializer = serializers.IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_reference = self.request.data['update_reference']
        issue_id = self.request.data['issue_id']
        new_value = self.request.data['new_value']

        issue = models.Issue.objects.get(id=issue_id)

        serializer = serializers.IssueSerializer(
            issue, data={update_reference: new_value}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.IssueSerializer


class IssueCommentView(views.APIView):
    """Use this endpoint to add issue comments in the backend."""

    def get(self):
        queryset = models.IssueComment.objects.all()
        comment_id = self.request.query_params.get('id', None)

        if comment_id is None:
            return queryset
        else:
            return queryset.filter(id=comment_id)

    def post(self, request):
        project = models.Project.objects.get(
            project_id=request.data['project_id'])
        request.data['project_id'] = project.id
        serializer = serializers.IssueCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_reference = self.request.data['update_reference']
        comment_id = self.request.data['comment_id']
        new_value = self.request.data['new_value']

        issue_comment = models.IssueComment.objects.get(id=comment_id)

        serializer = serializers.IssueCommentSerializer(
            issue_comment, data={update_reference: new_value}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.IssueCommentSerializer


class IssueReplyView(generics.ListCreateAPIView):
    """Use this endpoint to add projects in the backend."""

    def get_queryset(self):
        queryset = models.IssueReply.objects.all()
        reply_id = self.request.query_params.get('id', None)

        if reply_id is None:
            return queryset
        else:
            return queryset.filter(id=reply_id)

    def put(self, request):
        update_reference = self.request.data['update_reference']
        reply_id = self.request.data['reply_id']
        new_value = self.request.data['new_value']

        issue_reply = models.IssueReply.objects.get(id=reply_id)

        serializer = serializers.IssueReplySerializer(
            issue_reply, data={update_reference: new_value}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.IssueReplySerializer
