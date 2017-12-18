from django.shortcuts import render, redirect
from ..login_and_registration_app.models import Users

def index(request):
	empty = False
	if Users.objects.all().count() <= 1:
		empty = True
	user = Users.objects.get(id=request.session['user_id'])
	friends = user.friends.all()
	not_friends = Users.objects.all().exclude(id=user.id).exclude(id__in=friends)
	return render(request, "friends_app/index.html", {"user" : user, "not_friends" : not_friends, 'empty' : empty})	

def add_friend(request, user_id):
	user = Users.objects.get(id=request.session['user_id'])
	friend = Users.objects.get(id=user_id)
	user.friends.add(friend)
	return redirect('/friends')

def un_friend(request, user_id):
	user = Users.objects.get(id=request.session['user_id'])		
	friend = Users.objects.get(id=user_id)
	user.friends.remove(friend)
	return redirect('/friends')

def user_profile(request, user_id):
	user = Users.objects.get(id=user_id)
	return render(request, "friends_app/user_profile.html", {"user" : user})	

