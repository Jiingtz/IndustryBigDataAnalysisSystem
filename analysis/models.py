from django.db import models


# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=128, verbose_name='职位')  # 职位名称
    dutyStation = models.CharField(max_length=128, verbose_name='工作地点')  # 工作地点
    salary = models.CharField(max_length=64, verbose_name='薪资')  # 薪资
    experience = models.CharField(max_length=64, verbose_name='经验')  # 经验
    education = models.CharField(max_length=64, verbose_name='学历')  # 学历
    company = models.CharField(max_length=64, verbose_name='公司')  # 公司
    companyType = models.CharField(max_length=128, verbose_name='公司类型')  # 公司类型
    companyScale = models.CharField(max_length=64, verbose_name='公司规模')  # 公司规模
    technology = models.CharField(max_length=256, verbose_name='技术需求')  # 技术需求
    jobLabel = models.CharField(max_length=256, verbose_name='标签')  # 标签
