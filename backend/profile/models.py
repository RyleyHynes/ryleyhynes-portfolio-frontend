from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    summary = models.TextField()

class SkillCategory(models.Model):
    name = models.CharField(max_length=50)

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)

class Experience(models.Model):
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    highlights = models.TextField()

class Role(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="roles")
    title = models.CharField(max_length=100)
    range = models.CharField(max_length=50)

class Education(models.Model):
    school = models.CharField(max_length=100)
    detail = models.CharField(max_length=200)
    range = models.CharField(max_length=50)

class Project(models.Model):
    name = models.CharField(max_length=100)
    blurb = models.TextField()
    metrics = models.JSONField(default=list)
    stack = models.JSONField(default=list)
