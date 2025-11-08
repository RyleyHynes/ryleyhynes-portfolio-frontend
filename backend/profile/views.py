from rest_framework import viewsets
from .models import Profile, SkillCategory, Experience, Education, Project
from .serializers import ProfileSerializer, SkillCategorySerializer, ExperienceSerializer, EducationSerializer, ProjectSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SkillCategoryViewSet(viewsets.ModelViewSet):
    queryset = SkillCategory.objects.prefetch_related("skills").all()
    serializer_class = SkillCategorySerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.prefetch_related("roles").all()
    serializer_class = ExperienceSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
