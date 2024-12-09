from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Case, When, Count
from django.urls import reverse_lazy
from django.views.generic import ListView

from carLoudApp.projects.models import ProjectPost


class IndexView(ListView):
    model = ProjectPost
    template_name = 'common/index.html'

    def get_queryset(self):
        images = ProjectPost.objects.filter(project__private=False).annotate(like_count=Count('likes')).order_by('-like_count')[:8]
        return images

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('user-login')
    paginate_by = 7

    def get_queryset(self):
        user = self.request.user
        followed_users_pks = user.following.values_list('is_following', flat=True)

        queryset = ProjectPost.objects.filter(project__private=False, image__icontains='http://')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(project__title__icontains=search_query) |
                Q(project__user__username__icontains=search_query) |
                Q(caption__icontains=search_query)
            )

        queryset = queryset.annotate(
            is_followed_user=Case(
                When(project__user__pk__in=followed_users_pks, then=1),
                default=0
            )
        ).order_by('-is_followed_user', '-created_at')

        return queryset






