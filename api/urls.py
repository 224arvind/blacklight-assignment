from django.urls import re_path, path

from api.views import currWeekLeaderboard, lastWeekLeaderboard, userRank

urlpatterns = [
    path("curr-week-leaderboard", currWeekLeaderboard.as_view()),
    re_path(r"^last-week-leaderboard/$", lastWeekLeaderboard.as_view()),
    re_path(r"^user-rank/$", userRank.as_view()),
]