"""
read all student ans from database of the current requested exam
clean and stem them with the help of stemm.py
compare them  
"""
from configq.models import Question
from configq.misc_function import get_exam
from grader.src.stem import Stemmer
from grader.models import StudentAns



def auto_grade_all_ans(request, tobe_grade_question=None):
    """
    grade all ans if tobe_grade_question is not passed.
    else re-grade only passed question in tobe_grade_question  
    """
    stemmer = Stemmer()
    current_exam = get_exam(request)
    
    if not tobe_grade_question:
        questions = Question.objects.filter(exam = current_exam)
    else:
        print(tobe_grade_question.question_number)
        questions = Question.objects.filter(exam=current_exam, question_number=tobe_grade_question.question_number)
    # create list of tuple containing question num and stems of ans
    q_num_ans_stem = [(q.question_number, stemmer.sent_2_stem(q.questionAns)) for q in questions]
    # print(q_num_ans_stem)
    if not tobe_grade_question:
        student_ans_list = StudentAns.objects.filter(exam=current_exam)
    else:
        student_ans_list = StudentAns.objects.filter(exam=current_exam, question_num=tobe_grade_question.question_number)
    for student_ans in student_ans_list:
        question_num = student_ans.question_num
        print(question_num)
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


