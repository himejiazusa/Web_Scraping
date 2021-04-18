import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from mk_filename import mktxt_lists

# インディーズ商品ページURL
INDIES = {
    "オールデイズレコード": "catalog.php?srcrbl=odr&show_sort=rls",
    "A.M.P. タンゴ コレクション": "catalog.php?srcrbl=5109_",
    "BBQレコード": "catalog.php?srcrbl=5086_",
    "BSMFレコード": "catalog.php?srcrbl=5074_",
    "JET SET": "catalog.php?srcrbl=5099_",
    "MARQUEE INC.": "catalog.php?srcrbl=5009_",
    "MSI": "catalog.php?srcrbl=5005_",
    "P-VINE ブックス": "catalog.php?srcrbl=5120_",
    "P-VINE レコード": "catalog.php?srcrbl=5011_",
    "ROSE レコード": "catalog.php?srcrbl=5082_",
    "SHOUT! プロダクションズ": "catalog.php?srcrbl=5089_",
    "ぐらもくらぶ": "catalog.php?srcrbl=5136_",
    "その他の国内メーカー": "catalog.php?srcrbl=5999_5100_5121_5125_",
    "アライヴ ザ ライヴ": "catalog.php?srcrbl=5135_",
    "アルテス パブリッシング": "catalog.php?srcrbl=5107_",
    "インパートメント": "catalog.php?srcrbl=5081_",
    "ウルトラ ヴァイヴ": "catalog.php?srcrbl=5012_",
    "エアメイル/ワサビレコード": "catalog.php?srcrbl=5004_",
    "エム レコード": "catalog.php?srcrbl=5070_",
    "カケハシレコード": "catalog.php?srcrbl=5134_",
    "キャプテン トリップ": "catalog.php?srcrbl=5024_",
    "クール サウンド": "catalog.php?srcrbl=5003_",
    "クリンク レコード": "catalog.php?srcrbl=5000_",
    "クレオール ストリーム ミュージック": "catalog.php?srcrbl=5079_",
    "グッド ラヴィン": "catalog.php?srcrbl=5022_",
    "グラフィック社": "catalog.php?srcrbl=5117_",
    "サンドフィッシュ レコード": "catalog.php?srcrbl=5072_",
    "シャトーディスク": "catalog.php?srcrbl=5137_",
    "ショーボート/SKY STAION": "catalog.php?srcrbl=5008_",
    "シンコーミュージック": "catalog.php?srcrbl=5016_",
    "スーパーフジ ディスク": "catalog.php?srcrbl=5020_",
    "ストレンジ デイズ BOOK": "catalog.php?srcrbl=5017_5080_5106_",
    "ストレンジ デイズ CD": "catalog.php?srcrbl=5097_",
    "スペースシャワー ブックス": "catalog.php?srcrbl=5102_",
    "セレストレコード": "catalog.php?srcrbl=5026_",
    "ソウルガーデン レコード": "catalog.php?srcrbl=5132_",
    "ディスクユニオン": "catalog.php?srcrbl=5063_",
    "ディスクユニオン DU BOOKS": "catalog.php?srcrbl=5115_",
    "ハヤブサ ランディングス": "catalog.php?srcrbl=5036_",
    "パンヘッドアカデミー": "catalog.php?srcrbl=6008_",
    "ビーンズ レコード": "catalog.php?srcrbl=5033_",
    "ブリッジ": "catalog.php?srcrbl=5062_",
    "ボンバ レコード": "catalog.php?srcrbl=5007_",
    "ミューザック": "catalog.php?srcrbl=5091_",
    "ミュージック マガジン": "catalog.php?srcrbl=5014_",
    "モダーン ミュージック": "catalog.php?srcrbl=5025_",
    "ライスレコード": "catalog.php?srcrbl=5021_",
    "リットーミュージック": "catalog.php?srcrbl=5075_",
    "ロフトブックス": "catalog.php?srcrbl=5118_",
    "ヴィレッジ アゲイン": "catalog.php?srcrbl=5098_",
    "ヴィヴィド サウンド": "catalog.php?srcrbl=5001_",
    "芽瑠璃堂オリジナル": "catalog.php?srcrbl=6002_6005_6007_",
    "澤野工房": "catalog.php?srcrbl=5128_"
}
# 邦楽商品ページURL
JAPAN = {
    "ポップス": "catalog.php?srcgnr=POPS&srcrgl=jpn",
    "ロック": "catalog.php?srcgnr=ROCK&srcrgl=jpn",
    "R&B": "catalog.php?srcgnr=RnB&srcrgl=jpn",
    "ブルース": "catalog.php?srcgnr=BLUES&srcrgl=jpn",
    "ソウル": "catalog.php?srcgnr=SOUL&srcrgl=jpn",
    "ジャズ": "catalog.php?srcgnr=",
    "フォーク": "catalog.php?srcgnr=FOLK&srcrgl=jpn",
    "カントリー": "catalog.php?srcgnr=COUNTRY&srcrgl=jpn",
    "ワールド": "catalog.php?srcgnr=",
    "レゲエ": "catalog.php?srcgnr=REGGAE&srcrgl=jpn",
    "サントラ": "catalog.php?srcgnr=",
    "パンク": "catalog.php?srcgnr=PUNK&srcrgl=jpn",
    "オルタナティブ": "catalog.php?srcgnr=ALTERNATIVE&srcrgl=jpn",
    "クラブ": "catalog.php?srcgnr=CLUB&srcrgl=jpn",
    "ヒップホップ": "catalog.php?srcgnr=HIPHOP&srcrgl=jpn"
}

# ユーザー名とパスワードの指定
USER = '******'
PASS = '******'

home_page = "https://merurido.jp/"  # 芽瑠璃堂ホームページ
session = requests.session()  # セッションを開始
login_page = "https://merurido.jp/navi_index.php?navi=mypage"  # ログインページURL
data_list1 = []  # CSVリスト
data_list2 = []


# 芽瑠璃堂サイトにログイン
def auto_login(login_page):
    # ログイン情報
    login_info = {
        "login_mail": USER,
        "login_pass": PASS,
        "auto_login": "yes",
        "sblogin": "hdn"
    }
    res = session.post(login_page, data=login_info)
    res.raise_for_status()  # エラー回避
    return res, session, home_page


# ジャンルごとにCSV取得
def get_csv_txt(GENRE, list_name):
    for i in GENRE.values():
        cd_page = urljoin(home_page, i)  # 商品ページURL作成
        res = session.get(cd_page)  # 商品ページ取得
        res.raise_for_status()  # エラー回避

        #  BeautifulSoulでtextarea内文字取得
        soup = BeautifulSoup(res.content, "html.parser")
        links = soup.find("textarea")
        # BeautifulSoupオブジェクトを文字列に変換
        result = links.getText()
        list_name.append(result)
    return list_name


auto_login(login_page)

get_csv_txt(JAPAN, data_list1)
mktxt_lists(data_list1, "Merurido_J")

get_csv_txt(INDIES, data_list2)
mktxt_lists(data_list2, "Merurido_I")
