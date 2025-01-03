from django.contrib.auth import get_user_model
from rest_framework import serializers, permissions
from OpportunityHub.blog.models import BlogPost, Comment
from OpportunityHub.company.models import CompanyProfile
from OpportunityHub.candidates.models import Candidate
userModel = get_user_model()


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'user']
        # read_only_fields = ['first_name', 'last_name', 'pk']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_author(self, obj):
        # Check if the author is a candidate
        user = obj.author
        if user.role == 'candidate':
            candidate = user.candidate
            return CommentCandidateSerializer(candidate).data
        else:
            company = user.company
            return CommentCompanySerializer(company).data



class CommentCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'profile_picture', 'pk']

        # read_only_fields = ['first_name', 'last_name', 'pk']

class CommentCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'image', 'pk']


class CommentSerializerCreate(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content', 'author']

    def get_author(self, obj):
        # Check if the author is a candidate
        user = obj.author
        if user.role == 'candidate':
            candidate = user.candidate
            return CommentCandidateSerializer(candidate).data
        else:
            company = user.company
            return CommentCompanySerializer(company).data


class BlogPostSerializer(serializers.ModelSerializer):
    author = CandidateSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'
