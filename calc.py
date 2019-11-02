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
    return render_template('top.html')


@app.route('/common', methods=['GET', 'POST'])
def common():
    if request.method == 'POST':
        result = request.form
        my_credits = dict()
        for key, value in ALL_COMMON_SUBJECTS.items():
            if str(key) in result.keys():
                my_credits[key] = ALL_COMMON_SUBJECTS[key]['credits']
            else:
                my_credits[key] = 0

        sum_credit = dict()
        sum_credit['外国語'] = subjects_sum([10110010, 10110020, 10110030, 10110040, 10110050, 10110060, 10110070, 10110080, 10110090, 10110100, 10110110, 10110120, 10110130, 10110140, 10110150, 10110160, 10110170, 10110180, 10110190, 10110200, 10110210, 10110220, 10110230, 10110240, 10110250, 10110260, 10110270, 10110280, 10110290], my_credits)
        sum_credit['基礎科目'] = subjects_sum([10110010, 10110020, 10110030, 10110040, 10110050, 10110060, 10110070, 10110080, 10110090, 10110100, 10110110, 10110120, 10110130, 10110140, 10110150, 10110160, 10110170, 10110180, 10110190, 10110200, 10110210, 10110220, 10110230, 10110240, 10110250, 10110260, 10110270, 10110280, 10110290, 10120010, 10120020, 10130010, 10130020, 10130030, 10130040, 10130050, 10130060, 10140010, 10140020, 10140030], my_credits)
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

    else:
        return render_template('common.html', subjects=ALL_COMMON_SUBJECTS)


@app.route('/faculty_common')
def faculty_common():
    return render_template('faculty_common.html', subjects=FACULTY_COMMON_SUBJECTS)


@app.route('/faculty/<department>/<cource>', methods=['GET', 'POST'])
def major(department, cource):
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

        sum_credit = dict()
        sum_credit['学科専門科目'] = subjects_sum(my_credits.keys(), my_credits)
        sum_credit['導入科目'] = subjects_sum([22010010, 22010020, 22010030, 22010040, 22010050], my_credits)
        sum_credit['学部教養科目（人文・社会）'] = subjects_sum([22110010, 22110020, 22110030, 22110040, 22110050, 22110060, 22110070, 22110080, 22110090, 22110100, 22110110, 22110120, 22110130, 22110140, 22110150, 22110160, 22110170, 22120010, 22120020, 22120030, 22120040, 22120050, 22120060, 22120070, 22120080, 22120090, 22120100, 22120110, 22120120, 22120130, 22120140, 22120150, 22120160, 22120170, 22120180, 22120190], my_credits)
        sum_credit['学部教養科目（汎用的技能）'] = subjects_sum([22130010, 22130020, 22130030, 22130040, 22130050, 22130060, 22130070, 22130080], my_credits)
        sum_credit['学部教養演習'] = subjects_sum([22140010, 22140020, 22140030, 22140040, 22140050], my_credits)
        sum_credit['実践演習科目'] = subjects_sum([22410010, 22410020, 22410030, 22410040, 22410050, 22410060, 22410070, 22410080, 22410090, 22410100], my_credits)
        sum_credit['外国語必修'] = subjects_sum([ 22510010, 22510020, 22510030, 22510040, 22510050, 22510060, 22510070, 22510080], my_credits)
        sum_credit['外国語'] = subjects_sum([ 22510010, 22510020, 22510030, 22510040, 22510050, 22510060, 22510070, 22510080, 22510090, 22510100, 22510110, 22510120, 22510130, 22510140, 22510150, 22510160, 22510170, 22510180, 22510190, 22510200, 22510210, 22510220, 22510230, 22510240, 22510250, 22510260, 22510270, 22510280, 22510290, 22510300, 22510310, 22510320, 22510330, 22510340, 22510350, 22510360, 22510370, 22510380, 22510390, 22510400, 22520010, 22520020, 22520030, 22520040, 22520050, 22520060, 22520070, 22520080, 22520090, 22520100, 22520110, 22520120, 22520130, 22520140, 22520150, 22520160, 22520170, 22520180, 22520190, 22520200, 22520210, 22520220, 22520230, 22520240, 22520250], my_credits)
        sum_credit['♢印'] = subjects_sum([22010060, 22010070, 22140010, 22140020, 22140050, 22410010, 22410020, 22410030, 22410040, 22410050, 22410060, 22510340, 22510350, 22520090], my_credits)
        # excelで言うところのsheet3と4の単位が卒業要件単位にはまだ含まれてません。
        sum_credit['卒業要件単位（124単位以上）'] = subjects_sum(my_credits.keys(), my_credits)
        lack_credit = dict()
        lack_credit['学科専門科目'] = max(0, 94 - sum_credit['学科専門科目'])
        lack_credit['導入科目'] = max(0, 8 - sum_credit['導入科目'])
        lack_credit['学部教養科目（人文・社会）'] = max(0, 6 - sum_credit['学部教養科目（人文・社会）'])
        lack_credit['学部教養科目（汎用的技能）'] = max(0, 4 - sum_credit['学部教養科目（汎用的技能）'])
        lack_credit['学部教養演習'] = max(0, 2 - sum_credit['学部教養演習'])
        lack_credit['実践演習科目'] = max(0, 8 - sum_credit['実践演習科目'])
        lack_credit['外国語必修'] = max(0, 8 - sum_credit['外国語必修'])
        # 中国語あとで考えよう
        lack_credit['外国語'] = max(0, 20 - sum_credit['外国語'])
        lack_credit['♢印'] = max(0, 2 - sum_credit['♢印'])
        lack_credit['卒業要件単位（124単位以上）'] = max(0, 124 - sum_credit['卒業要件単位（124単位以上）'])

        if department == 'gi':
            sum_credit['基礎科目'] = subjects_sum([22220010, 22220020, 22220030, 22220040, 22220050, 22220060, 22220070, 22210010, 22210020, 22210030, 22210040, 22210050, 22210060, 22210070, 22210080, 22210090, 22210100, 22210110], my_credits)
            sum_credit['展開科目'] = subjects_sum([ 22310010, 22310020, 22310030, 22310040, 22310050, 22310060, 22310070, 22310080, 22310090, 22310100, 22310110, 22310120, 22310130, 22310140, 22310150, 22310160, 22310170, 22310180, 22310190, 22310200, 22310210,22320010, 22320020, 22320030, 22320040, 22320050, 22320060, 22320070, 22320080, 22320090, 22320100, 22320110,22330010, 22330020, 22330030, 22330040, 22330050, 22330060, 22330070], my_credits)

        elif department == 'gp':
            sum_credit['基礎科目'] = subjects_sum([22210010, 22210020, 22210030, 22210040, 22210050, 22210060, 22210070, 22210080, 22210090, 22210100, 22210110,#国際ビジネス観光基礎
                                                21210010, 21210020, 21210030, 21210040, 21210050, 21210060, 21210070, 21210080, 21210090 # 地域マネジメント基礎
                                                ], my_credits)
            sum_credit['展開科目'] = subjects_sum([22310010, 22310020, 22310030, 22310040, 22310050, 22310060, 22310070, 22310080, 22310090, 22310100, 22310110, 22310120, 22310130, 22310140, 22310150, 22310160, 22310170, 22310180, 22310190, 22310200, 22310210,21310010, 21310020, 21310030, 21310040, 21310050, 21310060, 21310070, 21310080, 21310090, 21310100, 21310110, 21310120, 21310130, 21310140, 21310150,22330010, 22330020, 22330030, 22330040, 22330050, 22330060, 22330070], my_credits)

        else:
            raise "department error"

        lack_credit['基礎科目'] = max(0, 12 - sum_credit['基礎科目'])
        lack_credit['展開科目'] = max(0, 34 - sum_credit['展開科目'])

        if cource == 'ic':
            sum_credit['コース必修'] = subjects_sum([22110080, 22130040, 22220010, 22220020, 22220060, 22330040], my_credits)
            sum_credit['コース展開科目'] = subjects_sum([22320010, 22320020, 22320030, 22320040, 22320050, 22320060, 22320070, 22320080, 22320090, 22320100, 22320110], my_credits)
            lack_credit['コース必修'] = max(0, 12 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])

        elif cource == 'rm':
            sum_credit['コース必修'] = subjects_sum([22120020, 22120070, 22120080, 22130020, 21210010, 21210040, 21210050, 21210070, 21210080, 21210090],  my_credits)
            sum_credit['コース展開科目'] = subjects_sum([21310010, 21310020, 21310030, 21310040, 21310050, 21310060, 21310070, 21310080, 21310090, 21310100, 21310110, 21310120, 21310130, 21310140, 21310150], my_credits)
            lack_credit['コース必修'] = max(0, 20 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])

        elif cource == 'bt':
            sum_credit['コース必修'] = subjects_sum([22120020, 22120070, 22120080, 22210040, 22210070, 22210080, 22210110], my_credits)
            sum_credit['コース展開科目'] = subjects_sum([ 22310010, 22310020, 22310030, 22310040, 22310050, 22310060, 22310070, 22310080, 22310090, 22310100, 22310110, 22310120, 22310130, 22310140, 22310150, 22310160, 22310170, 22310180, 22310190, 22310200, 22310210], my_credits)
            lack_credit['コース必修'] = max(0, 14 - sum_credit['コース必修'])
            lack_credit['コース展開科目'] = max(0, 12 - sum_credit['コース展開科目'])

        else:
            pass
            # raise "cource error"

        return render_template('faculty_common_result.html',
                               sum_credit=sum_credit,
                               lack_credit=lack_credit,
                               department=department,
                               cource=cource)

    else:
        if department == "gi":
            major_subjects = GLOBAL_INTERNATIONAL_SUBJECTS
        elif department == "gp":
            major_subjects = GLOBAL_POLICY_SUBJECTS
        else:
            raise

        return render_template('faculty_common.html',
                               subjects=FACULTY_COMMON_SUBJECTS,
                               major_subjects=major_subjects,
                               department=department,
                               cource=cource)


if __name__ == '__main__':
    app.run(debug=True)
