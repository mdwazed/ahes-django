import json

# class qConfig():

#     def __init__(self, semester, matNo, pageNo):
#         self.questions = []
#         self.semester = semester
#         self.matNo = matNo
#         self.pageNo = pageNo

#     def addQuestion(self, qParam):
#         self.questions.append(qParam)

#     def save(self):
#         with open('config.json', 'w') as outfile:
#             json.dump(self, outfile)
#             print('file written to disk')


config = {}
questions = []
candidatesMatNo = set()

def addParam(semester, matNo, pageNo):
    config['semester'] = semester
    config['matNo'] = matNo
    config['pageNo'] = pageNo

def addQuestion(qParam):
    questions.append(qParam)


def addCandidates(candidates):
    candidatesMatNo.update(candidates)

def saveConfig():
    with open('../config.json','w') as outfile:
        config['questionList'] = questions
        config['candidatesMatNo'] = list(candidatesMatNo)
        json.dump(config, outfile)
