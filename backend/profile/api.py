from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, SkillCategoryViewSet, ExperienceViewSet, EducationViewSet, ProjectViewSet

router = DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("skills", SkillCategoryViewSet)
router.register("experience", ExperienceViewSet)
router.register("education", EducationViewSet)
router.register("projects", ProjectViewSet)

urlpatterns = router.urls
