# IndustryBigDataAnalysisSystem
行业大数据分析系统
项目整体结构-->
从逻辑上分为五层
  1.置于底层的数据采集层使用selenium对Boss直聘，前程无忧和拉钩招聘网三个网站进行爬取，保证数据来源的可靠性，数据来源分布的普适性，为后续的数据分析提供良好的数据基础；
  2.在数据处理层，对爬取到的数据进行数据清洗，提炼数据中的关键数据，确保信息都是没有冗余以及脏数据；
  3.在数据存储层，采用elasticsearch对职位信息以及公司数据进行储存，同时结合Mysql数据库进行用户数据存储；
  4.在业务逻辑层，主要实现了基于sklearn的岗位薪资待遇预测和基于tf-idf的岗位推荐作为主要功能；
  5.在可视化层，基于django框架并结合使用echarts、jquery等前端技术搭建前端交互页面，来可视化功能成果。
  
实验部分-->
进行了以下三个实验：
  1.在实验一最高次幂对多项式回归的准确率、RMSE的影响中，根据准确率、RMSE两个评价指标，对多项式回归的最佳参数进行确定；
  2.同理，在实验二探究K值选择对K近邻回归的准确率、RMSE的影响中，根据评价指标对K近邻回归的准确率进行了确定；
  3.在实验三中，将实验一和实验二中获得到的两个最佳参数模型在准确率、RMSE对比选择表现最优的模型作为最终选择的模型。
