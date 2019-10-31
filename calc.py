from flask import Flask, render_template

app = Flask(__name__)
subjects = {
    10010010: {"name": "スタートアップ・セミナー", "credits": 1},
    10110010: {"name": "総合英語Ⅰa", "credits": 2},
    10110020: {"name": "総合英語Ⅰb", "credits": 2},
    10110030: {"name": "総合英語Ⅱa", "credits": 2},
    10110040: {"name": "総合英語Ⅱb", "credits": 2},
    10110050: {"name": "英語コミュニケーションa", "credits": 2},
    10110060: {"name": "英語コミュニケーションb", "credits": 2},
    10110070: {"name": "中国語Ⅰa", "credits": 2},
    10110080: {"name": "中国語Ⅰb", "credits": 2},
    10110090: {"name": "中国語Ⅱa", "credits": 2},
    10110100: {"name": "中国語Ⅱb", "credits": 2},
    10110110: {"name": "韓国語Ⅰa", "credits": 2},
    10110120: {"name": "韓国語Ⅰb", "credits": 2},
    10110130: {"name": "韓国語Ⅱa", "credits": 2},
    10110140: {"name": "韓国語Ⅱb", "credits": 2},
    10110150: {"name": "スペイン語Ⅰa", "credits": 2},
    10110160: {"name": "スペイン語Ⅰb", "credits": 2},
    10110170: {"name": "スペイン語Ⅱa", "credits": 2},
    10110180: {"name": "スペイン語Ⅱb", "credits": 2},
    10110190: {"name": "フランス語Ⅰa", "credits": 2},
    10110200: {"name": "フランス語Ⅰb", "credits": 2},
    10110210: {"name": "フランス語Ⅱa", "credits": 2},
    10110220: {"name": "フランス語Ⅱb", "credits": 2},
    10110230: {"name": "アカデミック・ジャパニーズ(Writing)", "credits": 2},
    10110240: {"name": "アカデミック・ジャパニーズ(Reading)", "credits": 2},
    10110250: {"name": "日本語A", "credits": 2},
    10110260: {"name": "日本語B", "credits": 2},
    10110270: {"name": "日本語C", "credits": 2},
    10110280: {"name": "日本語D", "credits": 2},
    10110290: {"name": "現代日本事情", "credits": 2},
    10120010: {"name": "情報リテラシー", "credits": 2},
    10120020: {"name": "生活と情報", "credits": 2},
    10130010: {"name": "運動と人間−講義", "credits": 2},
    10130020: {"name": "運動と人間−実技Ⅰ", "credits": 1},
    10130030: {"name": "運動と人間−実技Ⅱ", "credits": 1},
    10130040: {"name": "運動と人間−実技Ⅲ", "credits": 1},
    10130050: {"name": "運動と人間−実技Ⅳ", "credits": 1},
    10130060: {"name": "生活と健康", "credits": 2},
    10140010: {"name": "キャリアデザインⅠ", "credits": 2},
    10140020: {"name": "キャリアデザインⅡ", "credits": 2},
    10140030: {"name": "インターンシップ", "credits": 1},
    10140030: {"name": "人間と思想", "credits": 2},
    10210010: {"name": "人間と芸術−美術", "credits": 2},
    10210020: {"name": "人間と芸術−音楽", "credits": 2},
    10210030: {"name": "人間と芸術−文学", "credits": 2},
    10210040: {"name": "人間と文化", "credits": 2},
    10210050: {"name": "人間と心", "credits": 2},
    10220010: {"name": "人間と社会", "credits": 2},
    10220020: {"name": "社会と歴史", "credits": 2},
    10220030: {"name": "社会と政治", "credits": 2},
    10220040: {"name": "社会と経済", "credits": 2},
    10220050: {"name": "社会と法", "credits": 2},
    10220060: {"name": "日本国憲法", "credits": 2},
    10230010: {"name": "宇宙の科学", "credits": 2},
    10230020: {"name": "生物の科学", "credits": 2},
    10230030: {"name": "生活と科学", "credits": 2},
    10230040: {"name": "モノづくりデザインの基礎", "credits": 2},
    10240010: {"name": "環境論", "credits": 2},
    10240020: {"name": "ジェンダー論", "credits": 2},
    10240030: {"name": "グローバル化論", "credits": 2},
    10240040: {"name": "山梨学Ⅰ", "credits": 2},
    10240050: {"name": "山梨学Ⅱ", "credits": 2},
    10240060: {"name": "日本語の方言と山梨", "credits": 2},
    10250010: {"name": "プレゼンテーション", "credits": 2},
    10250020: {"name": "グループワークと自己表現", "credits": 2},
    10250030: {"name": "カウンセリング基礎", "credits": 2},
    10250040: {"name": "発達と教育の心理", "credits": 2},
    20010010: {"name": "国際関係論", "credits": 2},
    20010020: {"name": "平和と安全保証", "credits": 2},
    20010030: {"name": "文化とコミュニケーション", "credits": 2},
    20010040: {"name": "情報社会論", "credits": 2},
    20010050: {"name": "情報ネットワーク論", "credits": 2},
    20010060: {"name": "留学英語", "credits": 1},
    20010070: {"name": "共生社会論", "credits": 2},
    20010080: {"name": "韓国学概論", "credits": 2},
    20010090: {"name": "国際理解演習(韓国)", "credits": 4},
    20010100: {"name": "ソーシャルデザイン入門", "credits": 2},
    20020010: {"name": "地域ボランティア演習", "credits": 2},
    20020020: {"name": "コミュニケーション基礎", "credits": 2},
    20020030: {"name": "生と幸福", "credits": 2},
    20020040: {"name": "生涯スポーツ", "credits": 2},
    20030010: {"name": "リラクゼーション", "credits": 1},
    20030020: {"name": "救急法", "credits": 1},
    20030030: {"name": "災害支援", "credits": 1},
    20030040: {"name": "国際協力", "credits": 1},
}

@app.route('/')
def index():
    return render_template('common.html',subjects = subjects)


if __name__ == '__main__':
    app.run(debug = True)
