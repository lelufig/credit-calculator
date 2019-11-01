from flask import Flask, render_template, request
from subject_list import ALL_COMMON_SUBJECTS, FACULTY_COMMON_SUBJECTS, \
                         GLOBAL_INTERNATIONAL_SUBJECTS, GLOBAL_POLICY_SUBJECTS

app = Flask(__name__)


def subjects_sum(subject_id_list, my_credits):
    credits_sum = 0
    for subject_id in subject_id_list:
        credits_sum += my_credits[subject_id]
    return credits_sum


@app.route('/')
def index():
    return render_template('common.html', subjects=ALL_COMMON_SUBJECTS)

@app.route('/common_result', methods=['POST'])
def common_result():
    if request.method == 'POST':
        result = request.form
        my_credits = dict()
        for key, value in ALL_COMMON_SUBJECTS.items():
            if str(key) in result.keys():
                my_credits[int(key)] = ALL_COMMON_SUBJECTS[key]['credits']
            else:
                my_credits[key] = 0


        sum_credit = dict()
        sum_credit['外国語'] = subjects_sum([10110010, 10110020, 10110030, 10110040, 10110050, 10110060, 10110070, 10110080, 10110090, 10110100, 10110110, 10110120, 10110130, 10110140, 10110150, 10110160, 10110170, 10110180, 10110190, 10110200, 10110210, 10110220, 10110230, 10110240, 10110250, 10110260, 10110270, 10110280, 10110290,], my_credits)
        sum_credit['基礎科目'] = subjects_sum([ 10110010, 10110020, 10110030, 10110040, 10110050, 10110060, 10110070, 10110080, 10110090, 10110100, 10110110, 10110120, 10110130, 10110140, 10110150, 10110160, 10110170, 10110180, 10110190, 10110200, 10110210, 10110220, 10110230, 10110240, 10110250, 10110260, 10110270, 10110280, 10110290, 10120010, 10120020, 10130010, 10130020, 10130030, 10130040, 10130050, 10130060, 10140010, 10140020, 10140030,], my_credits)
        sum_credit['教養科目'] = subjects_sum([10210010, 10210020, 10210030, 10210040, 10210050, 10220010, 10220020, 10220030, 10220040, 10220050, 10220060, 10230010, 10230020, 10230030, 10230040, 10240010, 10240020, 10240030, 10240040, 10240050, 10240060, 10250010, 10250020, 10250030, 10250040, 20010010, 20010020, 20010030, 20010040, 20010050, 20010060, 20010070, 20010080, 20010090, 20010100, 20020010, 20020020, 20020030, 20020040, 20030010, 20030020, 20030030, 20030040], my_credits)
        sum_credit['スタートアップ・セミナー'] = subjects_sum([10010010], my_credits)
        sum_credit['単位数合計'] = subjects_sum([10010010, 10110010, 10110020, 10110030, 10110040, 10110050, 10110060, 10110070, 10110080, 10110090, 10110100, 10110110, 10110120, 10110130, 10110140, 10110150, 10110160, 10110170, 10110180, 10110190, 10110200, 10110210, 10110220, 10110230, 10110240, 10110250, 10110260, 10110270, 10110280, 10110290, 10120010, 10120020, 10130010, 10130020, 10130030, 10130040, 10130050, 10130060, 10140010, 10140020, 10140030, 10210010, 10210020, 10210030, 10210040, 10210050, 10220010, 10220020, 10220030, 10220040, 10220050, 10220060, 10230010, 10230020, 10230030, 10230040, 10240010, 10240020, 10240030, 10240040, 10240050, 10240060, 10250010, 10250020, 10250030, 10250040, 20010010, 20010020, 20010030, 20010040, 20010050, 20010060, 20010070, 20010080, 20010090, 20010100, 20020010, 20020020, 20020030, 20020040, 20030010, 20030020, 20030030, 20030040], my_credits)

        lack_credit = dict()
        lack_credit['外国語'] = max(0, 4 - sum_credit['外国語'])
        lack_credit['基礎科目'] = max(0, 4 - sum_credit['基礎科目'])
        lack_credit['教養科目'] = max(0, 8 - sum_credit['教養科目'])
        lack_credit['スタートアップ・セミナー'] = max(0, 1 - sum_credit['スタートアップ・セミナー'])
        lack_credit['単位数合計'] = max(0, 22 - sum_credit['単位数合計'])

    return render_template('common_result.html', sum_credit=sum_credit, lack_credit=lack_credit)










@app.route('faculty/<department>/<cource>')
def faculty_common(department, cource):
    pass


if __name__ == '__main__':
    app.run(debug=True)
