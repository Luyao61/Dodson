import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
import uuid
from lineup_test_2.models import Users, EyewitnessStimuli, Response


# Create your views here.
def index(request):

    return render(request, 'lineup_test_2/index.html')


def create_new_user(request):
    uid = uuid.uuid4().hex[:14].upper()
    while Users.objects.filter(pk=uid).exists():
        uid = uuid.uuid4().hex[:14].upper()

    new_user = Users(userId=uid)
    new_user.save()

    return HttpResponseRedirect(reverse('lineup_test_2:test_dir', args=(uid,)))


def test_dir(request, uid):
    category_list = EyewitnessStimuli.objects.values('category').distinct()
    context = {
        'uid': uid,
        'category_list': category_list,
    }
    return render(request, 'lineup_test_2/test_dir.html', context)


def generate_question(request, uid, category):
    chosen_set = []     # track lineup_number that has been used
    score_set = [60,80,100]
    race_set = ['W', 'B']

    question_set = []

    query_set_cate = EyewitnessStimuli.objects.filter(category=category)

    for i in range(6):
        query_set = query_set_cate.filter(score=score_set[int(i/2)], lineup_race=race_set[int(i % 2)])
        for n in chosen_set:
            query_set = query_set.exclude(lineup_number=n)

        q = random.choice(query_set)
        question_set.append(q)
        chosen_set.append(q.lineup_number)

    order = [0,1,2,3,4,5]
    random.shuffle(order)
    user = Users(userId=uid)
    for n in order:
        response = Response(user=user, question=question_set[n], category=category)
        response.save()
    return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, category,)))


def detail(request, uid, category):
    user = get_object_or_404(Users, pk=uid)
    q_set = user.response_set.filter(category=category).exclude(answer__isnull=True)
    q_num = len(q_set)
    print(q_num)

    if q_num == 6:
        return render(request, 'lineup_test_2/thankyou.html', context={'uid': uid})
    else:
        response = Response.objects.filter(user=user)[q_num]
        sample_q = response.question

        file_path = 'lineup_test_2/lineups/'
        lineup_number = sample_q.lineup_number
        if lineup_number[0] == 'W':
            file_path += 'faces_white/' + lineup_number[1] + '/'
        else:
            file_path += 'faces_black/' + lineup_number[1] + '/'

        lineup_order = sample_q.lineup_order.split(';')
        img_set_path = []
        chosen_face = ""
        for image_num in lineup_order:
            if int(image_num) == sample_q.chosen_face:
                chosen_face = file_path + image_num + '.jpg'

            img_set_path.append(file_path + image_num + '.jpg')
        stmt = sample_q.statement
        chosen_face = file_path + '5.jpg'

        context = {
            # 'sample' : sample_q,
            # 'image_path': file_path,
            'chosen': chosen_face,
            'lineup_order1': img_set_path[:3],
            'lineup_order2': img_set_path[3:],
            'statement': stmt,
            'uid': uid,
            'category': category,
        }
        return render(request, 'lineup_test_2/detail.html', context)


def record_answer(request, uid, category, a):
    ##
    print(a)
    user = get_object_or_404(Users, pk=uid)
    q_set = user.response_set.filter(category=category).exclude(answer__isnull=True)
    q_num = len(q_set)

    response = Response.objects.filter(user=user, category=category)[q_num]
    response.answer = a
    response.save()

    return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, category)))
