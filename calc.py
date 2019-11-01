from flask import Flask, render_template, request
from subject_list import ALL_COMMON_SUBJECTS, FACULTY_COMMON_SUBJECTS, \
                         GLOBAL_INTERNATIONAL_SUBJECTS, GLOBAL_POLICY_SUBJECTS

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('common.html', subjects=ALL_COMMON_SUBJECTS)


@app.route('faculty/<department>/<cource>')
def faculty_common(department, cource):
    pass


if __name__ == '__main__':
    app.run(debug=True)
