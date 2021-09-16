from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse
from analysis.models import Job
import os
from elasticsearch import Elasticsearch
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .salaryForecast import salary_predict
from .visualization import *
from .interface import *

# Create your views here.

es = Elasticsearch(["127.0.0.1:9200"])
RecommendationInterface = RecommendationInterface(
    'E:/大学学业/大四上/行业大数据分析实践/IndustryBigDataAnalysisSystem/analysis/data/job_profile.csv')


# 首页
def index(request):
    return render(request, 'index.html')


# 登录
def login(request):
    if request.method == 'POST':
        status = 0
        userEmail = request.POST.get('login_email')
        userPw = request.POST.get('login_pw')
        if '@' in userEmail:
            username = User.objects.filter(email=userEmail)[0].username
            user = auth.authenticate(username=username, password=userPw)
        else:
            user = auth.authenticate(username=userEmail, password=userPw)
        if user:
            url = request.GET.get('next')
            auth.login(request, user)
            if url:
                return_url = url
            else:
                return_url = reverse('index')
            ret = redirect(return_url)
            # ret.set_signed_cookie('is_login', '1', salt='s28', max_age=60 * 60 * 24)
            status = 1
            return ret
        else:
            error = '用户名或密码错误'
            return render(request, 'index.html', {'status': status})
    return render(request, 'index.html')


# 注销
def logout(request):
    ret = redirect('login')
    ret.delete_cookie('is_login')
    auth.logout(request)
    return ret


# 注册前检查用户名是否被占用
def check_username(request):
    username = request.GET.get('username')
    print(username)
    user = User.objects.filter(username=username)
    if user:
        return JsonResponse({'status': 'fail', 'msg': '此用户名已被占用'})
    else:
        return JsonResponse({'status': 'success', 'msg': '此用户名可用'})


# 注册
def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('register_name')
        user_pwd = request.POST.get('register_pw')
        user_email = request.POST.get('register_email')
        User.objects.create_user(username=user_name, password=user_pwd, email=user_email)
        return redirect('index')
    return render(request, 'register.html')


# 职位展示
def jobDetail(request):
    jobs = Job.objects.all()
    # 热门岗位
    hot_jobs = Job.objects.all().values_list('jobLabel').annotate(count=Count('jobLabel')).values_list(
        'jobLabel', 'count').order_by('-count')[:4]
    print('hot_job:', hot_jobs)
    # 获取当前页, 有则为page,无则默认为1
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(jobs, 20, request=request)
    jobPages = p.page(page)
    print(jobPages)
    return render(request, 'job-detail.html', locals())


# 职位搜索
def SearchJob(request):
    if request.method == 'POST':
        # 获取当前页, 有则为page,无则默认为1
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        searchKey = request.POST.get('keywords')
        # 若用户未输入关键词，则全局搜索
        if searchKey is None:
            searchKey = ''
        area = request.POST.get('area')
        salary = request.POST.get('salary')
        print(searchKey, area, salary)
        if area == '全国' and salary != '不限':
            jobs = Job.objects.filter(name__contains=searchKey, salary__contains=salary)
        elif area == '全国' and salary == '不限':
            jobs = Job.objects.filter(name__contains=searchKey)
        elif area != '全国' and salary == '不限':
            jobs = Job.objects.filter(name__contains=searchKey, dutyStation__contains=area)
        else:
            jobs = Job.objects.filter(name__contains=searchKey, dutyStation__contains=area, salary__contains=salary)
        # 热门岗位
        hot_jobs = Job.objects.filter(name__contains=searchKey).values_list('jobLabel').annotate(
            count=Count('jobLabel')).values_list(
            'jobLabel', 'count').order_by('-count')[:4]
        print('hot_job:', hot_jobs)
        p = Paginator(jobs, 20, request=request)
        jobPages = p.page(page)
        print(jobPages)
        return render(request, 'job-detail.html', locals())
    else:
        # 搜索后的翻页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        searchKey = request.GET.get('keywords')
        area = request.GET.get('area')
        salary = request.GET.get('salary')
        print(searchKey, area, salary)
        if area == '全国' and salary != '不限':
            jobs = Job.objects.filter(name__contains=searchKey, salary__contains=salary)
        elif area == '全国' and salary == '不限':
            jobs = Job.objects.filter(name__contains=searchKey)
        elif area != '全国' and salary == '不限':
            jobs = Job.objects.filter(name__contains=searchKey, dutyStation__contains=area)
        else:
            jobs = Job.objects.filter(name__contains=searchKey, dutyStation__contains=area, salary__contains=salary)
        # 热门岗位
        hot_jobs = Job.objects.filter(name__contains=searchKey).values_list('jobLabel').annotate(
            count=Count('jobLabel')).values_list(
            'jobLabel', 'count').order_by('-count')[:4]
        print('hot_job:', hot_jobs)
        p = Paginator(jobs, 20, request=request)
        jobPages = p.page(page)
        print(jobPages)
        return render(request, 'job-detail.html', locals())


# 分析可视化
def analyse(request):
    barData = getBar()
    pieData = getPie()
    areaData = getArea()
    radarData = getRadar()
    mapData = getMap()
    print(mapData)
    return render(request, 'analyse.html', locals())


def orientation2position(request):
    orientation = request.POST.get('orientation')
    with open('E:/大学学业/大四上/行业大数据分析实践/IndustryBigDataAnalysisSystem/analysis/data/salaryForecast.csv', 'r',
              encoding='UTF-8') as f:
        data = pd.read_csv(f)['标签']
    label_list = list(set(data))
    first_label_list = list(set([i.split('_')[0] for i in label_list]))
    label_dict = {}
    for i in first_label_list:
        second_label_list = [j.split('_')[1] for j in label_list if j.split('_')[0] == i]
        label_dict[i] = second_label_list
    positions = label_dict[orientation]
    print(positions)
    return JsonResponse({'positions': positions, 'length': len(positions)}, safe=False)


# 薪资预测
def salaryForecast(request):
    if request.method == 'POST':
        orientation = request.POST.get('orientation')
        position = request.POST.get('position')
        job_label = orientation + '_' + position
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        company_scale = request.POST.get('company_scale')
        salary = salary_predict(education, experience, company_scale, job_label)
        print(salary)
        return JsonResponse({'salary': ('%.2f' % salary)}, safe=False)
    return render(request, 'forecast.html')


# 职位预测
def jobForecast(request):
    if request.method == 'POST':
        education = request.POST.get('education')
        experience = request.POST.get('expertise').split('/')
        orientation = request.POST.get('orientation')
        feature = {'education': education, 'expertise': experience, 'orientation': orientation}
        positionId = RecommendationInterface.ReturnResult(feature)
        positions = []
        for p in positionId:
            position = [Job.objects.get(id=p).name, Job.objects.get(id=p).dutyStation, Job.objects.get(id=p).salary,
                        Job.objects.get(id=p).experience, Job.objects.get(id=p).education,
                        Job.objects.get(id=p).company, Job.objects.get(id=p).companyScale,
                        Job.objects.get(id=p).technology]
            positions.append(position)
        print(positions)
        return JsonResponse({'position': positions, 'length': len(positions)}, safe=False)
    return render(request, 'jobForecast.html')


# 全部公司查看
def companies(request):
    pictureName = os.listdir('E:\\大学学业\\大四上\\行业大数据分析实践\\IndustryBigDataAnalysisSystem\\static\\imgs\\company\\boss\\')
    companyList = [
        [i.split('.')[0], i.split('.')[0].split('_')[0],
         i.split('.')[0].split('_')[1], i.split('.')[0].split('_')[2]] for i in pictureName]
    print(companyList)
    return render(request, 'companies.html', {'companies': companyList})


# 公司详情
def companyDetail(request):
    companyName = request.POST.get('companyName')
    companyName = companyName.strip(' ').strip('\n').strip(' ')
    print(companyName)
    indexName = 'companies'
    try:
        query = es.search(body={
            "sort": [
                "_doc"
            ],
            "query": {
                "wildcard": {
                    "公司": {
                        "value": "*" + companyName + "*",
                    }
                }
            }
        }, index=indexName, scroll='1m', size=8)
        originList = query["hits"]["hits"]
        data = originList[0]['_source']['简介']
        print(data)
    except:
        print('暂无简介！')
        return JsonResponse({'introduction': '暂无简介！', 'link': 'https://baike.baidu.com/'}, safe=False)
    # print(data)
    return JsonResponse({'introduction': data, 'link': 'https://baike.baidu.com/'}, safe=False)


# 关键词相似推荐
def associate(request):
    searchData = request.POST.get('searchData')
    indexName = 'jobs'
    data = []
    try:
        query = es.search(body={
            "sort": [
                "_doc"
            ],
            "query": {
                "wildcard": {
                    "职位名称": {
                        "value": "*" + searchData + "*",
                    }
                }
            }
        }, index=indexName, scroll='1m', size=8)
        originList = query["hits"]["hits"]
        data = []
        for d in originList:
            data.append(d['_source']['职位名称'])
        print(data)
    except:
        print('联想中...')
    # print(data)
    return JsonResponse({'association': data}, safe=False)
