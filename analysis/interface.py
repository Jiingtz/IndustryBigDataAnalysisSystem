import pandas as pd


class RecommendationInterface():
    def __init__(self, filepath):
        self.datapath = filepath  # 数据所在位置

        self.job_profile = self.GetCsvData(self.datapath)
        self.inverted_table = self.CreateInvertedTable()  # 存储倒排索引

    def GetCsvData(self, filepath):
        '''
            读入原始数据
        :param filepath: 数据所在位置
        '''
        self.job_profile = pd.read_csv(filepath)
        return self.job_profile

    def ComputeScore(self, feature):
        '''
            由前端返回一个json字段{’education‘:str, 'expertise': list[], 'orientation': str}
            计算优先级返回得分岗位列表
        :param feature:  输入的特征 example : feature = {'education':'本科', 'expertise':['c++', 'python'], 'orientation':'后端开发'}
        :return:dict {jobid:score}  example :{0: 0.04406666316943898, 2: 0.029878535341733445,.....}

        '''
        weight = {'education': 0.2, 'expertise': 0.5, 'orientation': 0.3}
        scoredict = {}
        for featurename, featurecontent in feature.items():
            if featurename == 'education':
                for id, score in self.inverted_table[featurecontent]:
                    if id not in scoredict.keys():
                        scoredict[id] = weight[featurename] * score
                    else:
                        scoredict[id] += weight[featurename] * score
            elif featurename == 'expertise':
                # print(self.inverted_table.keys())
                if featurecontent not in list(self.inverted_table.keys()):
                    continue
                for id, score in self.inverted_table[featurecontent]:
                    if id not in scoredict.keys():
                        scoredict[id] = weight[featurename] * score
                    else:
                        scoredict[id] += weight[featurename] * score
            else:
                for id, score in self.inverted_table[featurecontent]:
                    if id not in scoredict.keys():
                        scoredict[id] = weight[featurename] * score
                    else:
                        scoredict[id] += weight[featurename] * score
        return scoredict

    def ReturnResult(self, feature, topk=10):
        '''
            获取特征为feature下的前topk个推荐结果
        :param feature:
        :param topk:
        :return:
        '''
        scoredict = self.ComputeScore(feature)
        result = sorted(scoredict.items(), key=lambda x: x[1], reverse=True)[:topk]
        return [i[0] for i in result]

    def CreateInvertedTable(self):
        # 构建倒排表
        inverted_table = {}
        for mid, weights in self.job_profile['weights'].iteritems():
            for tag, weight in eval(weights).items():
                _ = inverted_table.get(tag, [])
                _.append((mid, weight))
                inverted_table.setdefault(tag, _)
        return inverted_table  # {label : [(musicid, tfidf),()]}
