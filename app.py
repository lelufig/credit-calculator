from flask import Flask, render_template, request, redirect, send_from_directory
from subject_list import ALL_COMMON_SUBJECTS, FACULTY_COMMON_SUBJECTS, GLOBAL_INTERNATIONAL_SUBJECTS, GLOBAL_POLICY_SUBJECTS, REQUIREMENTS, GLOBAL_INTERNATIONAL_SUBJECTS_CATEGORY, GLOBAL_POLICY_SUBJECTS_CATEGORY
from collections import OrderedDict
from config import DEBUG
import os

app = Flask(__name__)
FACULTY_SUBJECTS = {}
FACULTY_SUBJECTS.update(FACULTY_COMMON_SUBJECTS)
FACULTY_SUBJECTS.update(GLOBAL_INTERNATIONAL_SUBJECTS)
FACULTY_SUBJECTS.update(GLOBAL_POLICY_SUBJECTS)


def subjects_sum(subject_id_list, my_credits):
    credits_sum = 0
    for subject_id in subject_id_list:
        credits_sum += my_credits[subject_id]
    return credits_sum


def detect_lack_subject_ids(requirements, my_credits):
    lack_subject_ids = []
    for subject_id in requirements:
        if my_credits[subject_id] == 0:
            lack_subject_ids.append(subject_id)
    return lack_subject_ids


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('top.html',
                           title='Credit Calculator')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        result = request.form
        department = result['department']
        cource = result['cource']
        chinese = result['chinese']
        return redirect(f'/common/{department}/{cource}/{chinese}')
    else:
        return render_template('form.html',
                               title='学科・コース情報入力 - Credit Calculator')


@app.route('/common/<department>/<cource>/<chinese>', methods=['GET', 'POST'])
def common(department, cource, chinese):
    if request.method == 'POST':
        result = request.form
        my_credits = dict()
        for key, value in ALL_COMMON_SUBJECTS.items():
            if str(key) in result.keys():
                my_credits[key] = ALL_COMMON_SUBJECTS[key]['credits']
            else:
                my_credits[key] = 0

        requirements = REQUIREMENTS['全学共通科目']

        sum_credit = OrderedDict()
        sum_credit['スタートアップ・セミナー'] = subjects_sum(requirements['スタートアップ・セミナー'], my_credits)
        sum_credit['外国語'] = subjects_sum(requirements['外国語'], my_credits)
        sum_credit['基礎科目'] = subjects_sum(requirements['基礎科目'], my_credits)
        sum_credit['教養科目'] = subjects_sum(requirements['教養科目'], my_credits)
        sum_credit['全学共通科目'] = subjects_sum(my_credits.keys(), my_credits) + int(result['10310010_credits'])

        lack_credit = OrderedDict()
        lack_credit['スタートアップ・セミナー'] = max(0, 1 - sum_credit['スタートアップ・セミナー'])
        lack_credit['外国語'] = max(0, 4 - sum_credit['外国語'])
        lack_credit['基礎科目'] = max(0, 8 - sum_credit['基礎科目'])
        lack_credit['教養科目'] = max(0, 8 - sum_credit['教養科目'])
        lack_credit['全学共通科目'] = max(0, 22 - sum_credit['全学共通科目'])

        common_sum = sum_credit['全学共通科目']

        lack_subject_ids = dict()
        lack_subject_ids['スタートアップ・セミナー'] = detect_lack_subject_ids(requirements['スタートアップ・セミナー'], my_credits)
        lack_subject_ids['外国語'] = detect_lack_subject_ids(requirements['外国語'], my_credits)
        lack_subject_ids['基礎科目'] = detect_lack_subject_ids(requirements['基礎科目'], my_credits)
        lack_subject_ids['教養科目'] = detect_lack_subject_ids(requirements['教養科目'], my_credits)
        lack_subject_ids['全学共通科目'] = detect_lack_subject_ids(my_credits.keys(), my_credits)

        return render_template('common_result.html',
                               title='全学共通科目の計算結果 - Credit Calculator',
                               subjects=ALL_COMMON_SUBJECTS,
                               sum_credit=sum_credit,
                               lack_credit=lack_credit,
                               lack_subject_ids=lack_subject_ids,
                               department=department,
                               cource=cource,
                               chinese=chinese,
                               common_sum=common_sum)

    else:
        return render_template('common.html',
                               title='全学共通科目の履修状況入力 - Credit Calculator',
                               subjects=ALL_COMMON_SUBJECTS,
                               department=department,
                               cource=cource,
                               chinese=chinese)


@app.route('/faculty_common')
def faculty_common():
    return render_template('faculty_common.html', subjects=FACULTY_COMMON_SUBJECTS)


@app.route('/faculty/<department>/<cource>/<chinese>/<int:common_sum>', methods=['GET', 'POST'])
def major(department, cource, chinese, common_sum):
    if request.method == 'POST':
        result = request.form
        my_credits = dict()
        for key, value in FACULTY_COMMON_SUBJECTS.items():
            if str(key) in result.keys():
                my_credits[key] = FACULTY_COMMON_SUBJECTS[key]['credits']
            else:
                my_credits[key] = 0

        if department == 'gi':
            for key, value in GLOBAL_INTERNATIONAL_SUBJECTS.items():
                if str(key) in result.keys():
                    my_credits[key] = GLOBAL_INTERNATIONAL_SUBJECTS[key]['credits']
                else:
                    my_credits[key] = 0
        else:
            for key, value in GLOBAL_POLICY_SUBJECTS.items():
                if str(key) in result.keys():
                    my_credits[key] = GLOBAL_POLICY_SUBJECTS[key]['credits']
                else:
                    my_credits[key] = 0

        requirements = REQUIREMENTS['学科専門科目']

        sum_credit = OrderedDict()
        sum_credit['学科専門科目'] = subjects_sum(my_credits.keys(), my_credits) + int(result['22530010_credits']) + int(result['22610010_credits'])
        sum_credit['導入科目'] = subjects_sum(requirements['導入科目'], my_credits)
        sum_credit['学部教養科目（人文・社会）'] = subjects_sum(requirements['学部教養科目（人文・社会）'], my_credits)
        sum_credit['学部教養科目（汎用的技能）'] = subjects_sum(requirements['学部教養科目（汎用的技能）'], my_credits)
        sum_credit['学部教養演習'] = subjects_sum(requirements['学部教養演習'], my_credits)
        sum_credit['実践演習科目'] = subjects_sum(requirements['実践演習科目'], my_credits)
        sum_credit['外国語必修'] = subjects_sum(requirements['外国語必修'], my_credits)

        if chinese == 'yes':
            sum_credit['中国語通年単位'] = subjects_sum(requirements['中国語通年単位'], my_credits)

        sum_credit['外国語'] = subjects_sum(requirements['外国語'], my_credits) + int(result['22530010_credits'])
        sum_credit['♢印'] = subjects_sum(requirements['♢印'], my_credits)

        lack_credit = OrderedDict()
        lack_credit['学科専門科目'] = max(0, 94 - sum_credit['学科専門科目'])
        lack_credit['導入科目'] = max(0, 8 - sum_credit['導入科目'])
        lack_credit['学部教養科目（人文・社会）'] = max(0, 6 - sum_credit['学部教養科目（人文・社会）'])
        lack_credit['学部教養科目（汎用的技能）'] = max(0, 4 - sum_credit['学部教養科目（汎用的技能）'])
        lack_credit['学部教養演習'] = max(0, 2 - sum_credit['学部教養演習'])
        lack_credit['実践演習科目'] = max(0, 8 - sum_credit['実践演習科目'])
        lack_credit['外国語必修'] = max(0, 8 - sum_credit['外国語必修'])

        lack_subject_ids = dict()
        lack_subject_ids['学科専門科目'] = detect_lack_subject_ids(my_credits.keys(), my_credits)
        lack_subject_ids['導入科目'] = detect_lack_subject_ids(requirements['導入科目'], my_credits)
        lack_subject_ids['学部教養科目（人文・社会）'] = detect_lack_subject_ids(requirements['学部教養科目（人文・社会）'], my_credits)
        lack_subject_ids['学部教養科目（汎用的技能）'] = detect_lack_subject_ids(requirements['学部教養科目（汎用的技能）'], my_credits)
        lack_subject_ids['学部教養演習'] = detect_lack_subject_ids(requirements['学部教養演習'], my_credits)
        lack_subject_ids['実践演習科目'] = detect_lack_subject_ids(requirements['実践演習科目'], my_credits)
        lack_subject_ids['外国語必修'] = detect_lack_subject_ids(requirements['外国語必修'], my_credits)

        if chinese == 'yes':
            lack_credit['中国語通年単位'] = max(0, 8 - sum_credit['中国語通年単位'])
            lack_subject_ids['中国語通年単位'] = detect_lack_subject_ids(requirements['中国語通年単位'], my_credits)

        lack_credit['外国語'] = max(0, 20 - sum_credit['外国語'])
        lack_credit['♢印'] = max(0, 2 - sum_credit['♢印'])

        lack_subject_ids['外国語'] = detect_lack_subject_ids(requirements['外国語'], my_credits)
        lack_subject_ids['♢印'] = detect_lack_subject_ids(requirements['♢印'], my_credits)

        if department == 'gi':
            sum_credit['基礎科目'] = subjects_sum(requirements['基礎科目']['gi'], my_credits)
            sum_credit['展開科目'] = subjects_sum(requirements['展開科目']['gi'], my_credits)
            lack_subject_ids['基礎科目'] = detect_lack_subject_ids(requirements['基礎科目']['gi'], my_credits)
            lack_subject_ids['展開科目'] = detect_lack_subject_ids(requirements['展開科目']['gi'], my_credits)

        elif department == 'gp':
            sum_credit['基礎科目'] = subjects_sum(requirements['基礎科目']['gp'], my_credits)
            sum_credit['展開科目'] = subjects_sum(requirements['展開科目']['gp'], my_credits)
            lack_subject_ids['基礎科目'] = detect_lack_subject_ids(requirements['基礎科目']['gp'], my_credits)
            lack_subject_ids['展開科目'] = detect_lack_subject_ids(requirements['展開科目']['gp'], my_credits)

        else:
            raise "department error"

        lack_credit['基礎科目'] = max(0, 12 - sum_credit['基礎科目'])
        lack_credit['展開科目'] = max(0, 34 - sum_credit['展開科目'])

        if cource == 'ic':
            sum_credit['コース必修'] = subjects_sum(requirements['コース必修']['ic'], my_credits)
            sum_credit['コース展開科目'] = subjects_sum(requirements['コース展開科目']['ic'], my_credits)
            lack_credit['コース必修'] = max(0, 12 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])
            lack_subject_ids['コース必修'] = detect_lack_subject_ids(requirements['コース必修']['ic'], my_credits)
            lack_subject_ids['コース展開科目'] = detect_lack_subject_ids(requirements['コース展開科目']['ic'], my_credits)

        elif cource == 'rm':
            sum_credit['コース必修'] = subjects_sum(requirements['コース必修']['rm'], my_credits)
            sum_credit['コース展開科目'] = subjects_sum(requirements['コース展開科目']['rm'], my_credits)
            lack_credit['コース必修'] = max(0, 20 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])
            lack_subject_ids['コース必修'] = detect_lack_subject_ids(requirements['コース必修']['rm'], my_credits)
            lack_subject_ids['コース展開科目'] = detect_lack_subject_ids(requirements['コース展開科目']['rm'], my_credits)

        elif cource == 'bt':
            sum_credit['コース必修'] = subjects_sum(requirements['コース必修']['bt'], my_credits)
            sum_credit['コース展開科目'] = subjects_sum(requirements['コース展開科目']['bt'], my_credits)
            lack_credit['コース必修'] = max(0, 14 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])
            lack_subject_ids['コース必修'] = detect_lack_subject_ids(requirements['コース必修']['bt'], my_credits)
            lack_subject_ids['コース展開科目'] = detect_lack_subject_ids(requirements['コース展開科目']['bt'], my_credits)

        else:
            raise "cource error"

        sum_credit['卒業要件単位（124単位以上）'] = subjects_sum(my_credits.keys(), my_credits) + int(result['22530010_credits']) + int(result['22610010_credits']) + common_sum
        lack_credit['卒業要件単位（124単位以上）'] = max(0, 124 - sum_credit['卒業要件単位（124単位以上）'])

        return render_template('faculty_common_result.html',
                               title='学科専門科目の計算結果 - Credit Calculator',
                               subjects=FACULTY_SUBJECTS,
                               sum_credit=sum_credit,
                               lack_credit=lack_credit,
                               lack_subject_ids=lack_subject_ids,
                               department=department,
                               cource=cource,
                               chinese=chinese)

    else:
        if department == "gi":
            major_subjects = GLOBAL_INTERNATIONAL_SUBJECTS_CATEGORY
        elif department == "gp":
            major_subjects = GLOBAL_POLICY_SUBJECTS_CATEGORY
        else:
            raise

        return render_template('faculty_common.html',
                               title='学科専門科目の履修状況入力 - Credit Calculator',
                               subjects=FACULTY_COMMON_SUBJECTS,
                               major_subjects=major_subjects,
                               department=department,
                               cource=cource,
                               chinese=chinese,
                               common_sum=common_sum)


if __name__ == '__main__':
    app.run(debug=DEBUG)
