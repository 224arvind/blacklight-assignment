from django.shortcuts import render
from django.views import View
from datetime import date, timedelta
from .models import UserInfo
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
def get_latest_entries(user_info_queryset):
    user_info_queryset = user_info_queryset.order_by('uid', '-timestamp')
    latest_user_info = []
    curr_uid = ''
    for user_info in user_info_queryset:
        if curr_uid != user_info.uid:
            latest_user_info.append(user_info)
            curr_uid = user_info.uid
    latest_user_info.sort(reverse=True, key=lambda x:x.score)

    return latest_user_info

class currWeekLeaderboard(View):
    def get(self, request):
        curr_date = date.today()
        weekday_num = curr_date.weekday()
        curr_week_start_date = curr_date - timedelta(days=weekday_num)
        user_info_queryset = get_latest_entries(UserInfo.objects.filter(timestamp__gte=curr_week_start_date))
        
        response_text = ''
        response_json = {'leaderboard':[]}
        count = 0
        for user_info in user_info_queryset:
            if count == 200:
                break
            # response_text += (
            #     "UID: "
            #     + user_info.uid
            #     + " Name: "
            #     + user_info.name
            #     + " Score: "
            #     + str(user_info.score)
            #     + " Country: "
            #     + user_info.country
            #     + "\n"
            # )
            response_json['leaderboard'].append({
				'uid': user_info.uid,
				'name': user_info.name,
				'score': user_info.score,
				'country': user_info.country,
				'timestamp': user_info.timestamp.strftime('%d/%m/%Y')
			})
            count += 1
        return JsonResponse(response_json)

class lastWeekLeaderboard(View):
    def get(self, request):
        country = request.GET.get('country', '')
        curr_date = date.today()
        weekday_num = curr_date.weekday()
        last_week_start_date = curr_date - timedelta(days=weekday_num+7)
        last_week_end_date = last_week_start_date + timedelta(days=6)
        user_info_queryset = get_latest_entries(UserInfo.objects.filter(
            timestamp__gte=last_week_start_date, timestamp__lte=last_week_end_date, country=country
        ))
        
        response_text = ''
        response_json = {'leaderboard':[]}
        count = 0
        for user_info in user_info_queryset:
            if count == 200:
                break
            response_json['leaderboard'].append({
				'uid': user_info.uid,
				'name': user_info.name,
				'score': user_info.score,
				'country': user_info.country,
				'timestamp': user_info.timestamp.strftime('%d/%m/%Y')
			})
            count += 1
        return JsonResponse(response_json)

    
class userRank(View):
    def get(self, request):
        uid = request.GET.get('uid', '')
        latest_user_info = get_latest_entries(UserInfo.objects.all())
        rank = 1
        for user_info in latest_user_info:
            if user_info.uid != uid:
                rank += 1
            else:
                break
        return JsonResponse({'rank':rank})
