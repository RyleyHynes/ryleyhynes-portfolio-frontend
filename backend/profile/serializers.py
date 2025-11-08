from rest_framework import serializers
from .models import Profile, SkillCategory, Skill, Experience, Role, Education, Project

class SkillSerializer(serializers.ModelSerializer):
    class Meta: model = Skill; fields = "__all__"

class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    class Meta: model = SkillCategory; fields = ["id", "name", "skills"]

class RoleSerializer(serializers.ModelSerializer):
    class Meta: model = Role; fields = ["id", "title", "range"]

class ExperienceSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    class Meta: model = Experience; fields = ["id", "company", "location", "highlights", "roles"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: model = Profile; fields = "__all__"

class EducationSerializer(serializers.ModelSerializer):
    class Meta: model = Education; fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model = Project; fields = "__all__"
