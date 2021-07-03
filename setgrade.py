# coding=utf-8
import csv
import json
import time
import urllib, urllib.parse
import network

def merge(x, y):
    z = {**x, **y}  
    return z

_data = u".\\score_list.csv"
host_url = 'https://elearn2.fju.edu.tw/'
keyword_epoch = u'第2章作业-2'
web_work = network.MyWeb()
homework_id = '1146466'
course_id = '211946'
cookie = '_ga_MR2C5GXFNE=GS1.1.1607527276.4.0.1607527278.0; AMCV_8E929CC25A1FB2B30A495C97@AdobeOrg=1687686476|MCIDTS|18774|MCMID|19569004409626950860973084268519580203|MCAAMLH-1622623969|11|MCAAMB-1622623969|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1622026369s|NONE|MCAID|NONE|vVersion|3.0.0; __gads=ID=ee3a715645d78dd5:T=1622019191:S=ALNI_Ma9Y-52Pf82P3v-XqiaiOk0NvmxwQ; utag_main=v_id:0179a7e05a030016555a5f0a417003073005106b00978$_sn:1$_se:13$_ss:0$_st:1622021237937$ses_id:1622019168773;exp-session$_pn:7;exp-session$vapi_domain:fju.edu.tw; __dtsu=51A016157775948A2C241DCDAE35286E; _cc_id=b7b0fe2616dfa66f8f85602496a2576a; optimizelyEndUserId=oeu1622798454321r0.8011179797526045; amplitude_id_9f6c0bb8b82021496164c672a7dc98d6_edmfju.edu.tw=eyJkZXZpY2VJZCI6ImUxNTYzZTAwLWEyN2YtNDI5NS1iNjUzLTQ5ZmE2NDI2MGU1MVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYyMjc5ODYzMjUxOCwibGFzdEV2ZW50VGltZSI6MTYyMjc5ODc0MzQxMSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6Niwic2VxdWVuY2VOdW1iZXIiOjZ9; amplitude_id_408774472b1245a7df5814f20e7484d0fju.edu.tw=eyJkZXZpY2VJZCI6ImI2MGI3M2EyLTQ5OGYtNDBhOC1hZGNlLWQ2MjI4MmUxZDc3YyIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjIyNzk4NDU1MjI2LCJsYXN0RXZlbnRUaW1lIjoxNjIyNzk4NzYxMjYzLCJldmVudElkIjoyMiwiaWRlbnRpZnlJZCI6NDMsInNlcXVlbmNlTnVtYmVyIjo2NX0=; _ga_468JNHR1KE=GS1.1.1623484503.1.1.1623484522.0; _ga=GA1.3.1413307594.1563160832; _gat=1; session=V2-1-6539d396-91b9-431b-9e2b-71bd8b1695cd.MjIxMzU4.1625305433.hfIb2yH0JXthW4hMD2qxzvgPPqU'

if __name__ == '__main__':

    score_list = []

    with open(_data, encoding='utf-8') as f:
        reader = csv.reader(f)
        # reader = unicodecsv.reader(f, encoding='utf-8', delimiter=',')
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

    # for score_item in score_list:
    #     student_score = str(float(score_item['score_val']))
    #     url = host_url + '/api/course/activities/' + homework_id + '/submission/score?fields=id,score,instructor_comment,rubric_score,final_score'
    #     dictdata = {"score": student_score, "reviewer_comment": '', "student_id": score_item["stu_id"]}
    #     content_type = {'Content-Type': 'application/json;charset=UTF-8'}
    #     print(url)
    #     res = web_work.putJson(url, dictdata, dict(list(header.items()) + list(content_type.items())))
    #     # result = res.read()
    #     print (res)

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
            print (student_id + 'not found')
        else:
            keywords = urllib.parse.quote((keyword_epoch + '_' + student_number + '_' + student_name).encode('UTF8'))
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
                    print (student_number + 'not found2')

                url = host_url + '/api/course/activities/' + homework_id + '/submission/score?fields=id,score,instructor_comment,rubric_score,final_score'
                dictdata = {"score": student_score, "reviewer_comment": '', "uploads": upload_ids, "student_id": student_id}
                content_type = {'Content-Type': 'application/json;charset=UTF-8'}

                res = web_work.putJson(url, dictdata, dict(list(header.items()) + list(content_type.items())))
                result = res.read()
                print (result)
                pass
