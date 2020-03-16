# coding=utf-8
import csv
import json
import time
import urllib
import network

_data = u"E:\\第2章作业-2\\score_list.csv"
host_url = 'http://courses.zju.edu.cn:8060'
keyword_epoch = u'第2章作业-2'
web_work = network.MyWeb()
homework_id = ''
course_id = ''
cookie = ''

if __name__ == '__main__':

    score_list = []

    with open(_data) as f:
        reader = csv.reader(f)
        # 读取一行，下面的reader中已经没有该行了
        head_row = next(reader)
        for row in reader:
            # 行号从1开始
            stu_id = row[0]
            name = row[1]
            score_val = row[2]
            score_list.append({"stu_id": stu_id, "name": name, "score_val": score_val})

    t = time.time()
    timestamp = int(round(t * 1000))

    header = {
        'Cookie': cookie
        # 'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    }
    url = host_url + '/api/homework/' + homework_id + '/student-submissions?need_uploads_size=true&no_cache=' + str(
        timestamp)
    res = web_work.get(url, header)
    result = res.read()
    res_json = json.loads(result)
    homework_items = res_json['submissions']

    url = host_url + '/api/course/' + course_id + '/students?no_cache=' + str(timestamp) + '&ignore_avatar=true'
    res = web_work.get(url, header)
    result = res.read()
    res_json = json.loads(result)
    student_items = res_json['students']

    for homework_item in homework_items:
        student_id = homework_item['created_by']['id']
        student_name = ''
        student_number = ''
        for student_item in student_items:
            if student_item['id'] == student_id:
                student_name = student_item['name']
                student_number = student_item['user_no']
                break

        if student_name == '' or student_number == '':
            print student_id + 'not found'
        else:
            keywords = urllib.quote((keyword_epoch + '_' + student_number + '_' + student_name).encode('UTF8'))
            conditions = '%7B%22keyword%22:%22' + keywords + '%22,%22includeSlides%22:false,%22limitTypes%22:%5B%5D,%22fileType%22:%22all%22,%22parentId%22:0,%22resourceType%22:null,%22filters%22:%5B%5D,%22linkTypes%22:%5B%5D%7D'
            url = host_url + '/api/user/resources?no_cache=' + str(
                timestamp) + '&conditions=' + conditions + '&page=1&page_size=10'
            res = web_work.get(url, header)
            result = res.read()
            res_json = json.loads(result)
            upload_items = res_json['uploads']
            upload_ids = []
            for upload_item in upload_items:
                upload_ids.append(upload_item['id'])

            marked_submitted = homework_item['marked_submitted']
            if marked_submitted is True:
                student_score = ''
                for score_item in score_list:
                    if score_item['stu_id'] == student_number:
                        student_score = str(float(score_item['score_val']))
                        break
                if student_score == '':
                    print student_number + 'not found2'

                url = host_url + '/api/course/activities/' + homework_id + '/submission/score?fields=id,score,instructor_comment,rubric_score,final_score'
                dictdata = {"score": student_score, "reviewer_comment": '', "uploads": upload_ids, "student_id": student_id}
                content_type = {'Content-Type': 'application/json;charset=UTF-8'}

                res = web_work.putJson(url, dictdata, dict(header.items() + content_type.items()))
                result = res.read()
                print result
                pass
