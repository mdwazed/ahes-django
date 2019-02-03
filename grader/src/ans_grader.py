"""
read all student ans from database of the current requested exam
clean and stem them with the help of stemm.py
compare them  
"""
from grader.src.stem import Stemmer
from configq.misc_function import get_exam
from grader.models import StudentAns
from configq.models import Question



def grade_all_ans(request):
    stemmer = Stemmer()
    current_exam = get_exam(request)
    # print(current_exam)
    questions = Question.objects.filter(exam = current_exam)
    # create list of tuple containing question num and stems of ans
    q_num_ans_stem = [(q.question_number, stemmer.sent_2_stem(q.questionAns)) for q in questions]
    # print(q_num_ans_stem)
    student_ans_list = StudentAns.objects.filter(exam=current_exam)
    for student_ans in student_ans_list:
        question_num = student_ans.question_num
        current_q_stems = [x[1] for x in q_num_ans_stem if x[0] == question_num]
        confidence = stemmer.get_confidence(current_q_stems[0], student_ans.students_ans)
        # print(confidence) 
        student_ans.matching_confidence = confidence
        question = questions.get(question_number=question_num)
        if confidence > question.threshold:
            auto_grade = question.allotedMarks
        else:
            auto_grade = 0
        student_ans.auto_grade = auto_grade
        student_ans.save()


