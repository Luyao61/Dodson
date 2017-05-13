import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
import uuid
from lineup_test_2.models import User, EyewitnessStimuli, Response, SecretCode


# Create your views here.
def index(request):

    return render(request, 'lineup_test_2/index.html')


def create_new_user(request):
    category_list = ['O1', 'Omany', 'R', 'U1', 'F']
    uid = uuid.uuid4().hex[:14].upper()
    while User.objects.filter(pk=uid).exists():
        uid = uuid.uuid4().hex[:14].upper()

    random_category = random.choice(category_list)

    if random.randint(1,2) == 1:
        new_user = User(userId=uid, StatementType=True, category=random_category)
    else:
        new_user = User(userId=uid, StatementType=False, category=random_category)

    new_user.save()

    # return HttpResponseRedirect(reverse('lineup_test_2:test_dir', args=(uid,)))
    return HttpResponseRedirect(reverse('lineup_test_2:instruction', args=(uid, 1)))


def test_dir(request, uid):
    context = {
        'uid': uid,
    }
    """
    user = get_object_or_404(User, pk=uid)

    # removed by lz, on 08/08
    # category_list = EyewitnessStimuli.objects.values('category').distinct()
    lineup_category = [user.category]


    count = 0
    finished = True
    # removed by lz, on 08/08
    # for cate in ["O1", "Omany", "R"]:
    for cate in lineup_category:
        # q_set = user.response_set.filter(category=cate)
        q_set = user.response_set.all()
        if len(q_set) == 0: # test has not been generated yet.
            finished = False
            break

        # q_set = user.response_set.filter(category=cate).filter(answer__isnull=True)
        q_set = user.response_set.all().filter(answer__isnull=True)
        # print(len(q_set))
        count += len(q_set)

    # print(count)
    if finished and count == 0:
        context = generate_survey_content(context)
        return render(request, 'lineup_test_2/survey.html', context)
    else:
        # removed by lz, on 08/08
        # context['category_list'] = category_list
        context['category_list'] = lineup_category
        return render(request, 'lineup_test_2/test_dir.html', context)
    """
    context = generate_survey_content(context)
    return render(request, 'lineup_test_2/survey.html', context)


def generate_question(request, uid):
    user = get_object_or_404(User, pk=uid)
    lineup_category = user.category
    q_set = user.response_set.all()
    if len(q_set) != 0:
        return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, lineup_category,)))
    query_set_cate = EyewitnessStimuli.objects.filter(category=lineup_category)
    race_set = ['W', 'B']
    question_set = []

    for race in race_set:
        chosen_set = []  # track lineup_number that has been used
        query_set = query_set_cate.filter(lineup_race=race)
        if len(query_set) == 3:
            for q in query_set:
                question_set.append(q)
        else:
            for _ in range(3):
                for n in chosen_set:
                    query_set = query_set.exclude(lineup_number=n)
                q = random.choice(query_set)
                question_set.append(q)
                chosen_set.append(q.lineup_number)

    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    user = User(userId=uid)

    for n in order:
        response = Response(user=user, question=question_set[n])
        response.save()
    '''
    user = get_object_or_404(User, pk=uid)
    q_set = user.response_set.filter(category=category)
    if len(q_set) != 0:
        return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, category,)))

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
    user = User(userId=uid)
    for n in order:
        response = Response(user=user, question=question_set[n], category=category)
        response.save()
    return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, category,)))
    '''
    return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, lineup_category,)))


def detail(request, uid, category):
    user = get_object_or_404(User, pk=uid)
    # q_set = user.response_set.filter(category=user.category).exclude(answer__isnull=True)
    q_set = user.response_set.all().exclude(answer__isnull=True)

    q_num = len(q_set)
    # print(q_num)

    statement_type = user.StatementType

    if q_num == 6:
        context = {
            'uid': uid,
            'mode': 3,
        }
        # return render(request, 'lineup_test_2/instruction.html', context)
        return HttpResponseRedirect(reverse('lineup_test_2:instruction', args=(uid, 3)))
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

        if statement_type:
            stmt = sample_q.statement
        else:
            stmt = sample_q.statementOnly

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

    # print(a)
    user = get_object_or_404(User, pk=uid)
    # q_set = user.response_set.filter(category=category).exclude(answer__isnull=True)
    q_set = user.response_set.all().exclude(answer__isnull=True)
    q_num = len(q_set)

    # response = Response.objects.filter(user=user, category=category)[q_num]
    response = Response.objects.filter(user=user)[q_num]
    response.answer = a
    response.save()

    return HttpResponseRedirect(reverse('lineup_test_2:detail', args=(uid, category)))


def instruction(request, uid, mode):
    # print (mode)
    context = {
        'mode': mode,
        'uid': uid,
    }
    return render(request, 'lineup_test_2/instruction.html', context)


def example(request, uid):
    return render(request, 'lineup_test_2/example.html', context={'uid':uid})


def submit_survey(request, uid):
    # print(request)
    # print(request.POST.get("sex"))
    # print(request.POST.get("birthyear"))
    # print(request.POST.get("device"))
    # print(request.POST.get("race"))

    user = get_object_or_404(User, pk=uid)
    user.sex = request.POST.get("sex")
    user.birth_year = request.POST.get("birthyear")
    user.device = request.POST.get("device")
    user.race = request.POST.get("race")
    user.comments = request.POST.get("comment")[:100]
    user.save()

    codes = SecretCode.objects.filter(valid=True)
    if len(codes) >= 1:
        code = random.choice(codes).code
    else:
        code = None
    # return HttpResponse("Thank you for participating this survey!\n You may now close your browser.")
    return render(request, 'lineup_test_2/final_page.html', context={'code':code})


def generate_survey_content(context):
    b_year = [i for i in range(1900,2018)]
    b_year.reverse()
    race = ['Whte/Caucasian', 'Black/African-American', 'Hispanic', 'Asian/Pacific Islander', 'Other']
    device = ['desktop', 'laptop', 'iphone/smartphone', 'ipad/tablet']
    context['year_list'] = b_year
    context['race_list'] = race
    context['device_list'] = device

    return context


def record_example(request, uid, a):
    user = get_object_or_404(User, pk=uid)
    user.example_response = a
    user.save()

    return HttpResponseRedirect(reverse('lineup_test_2:instruction', args=(uid, 2)))
