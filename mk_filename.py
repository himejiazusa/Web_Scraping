import csv
import datetime

export_file_path = '/Users/apple/Desktop/Finish/'  # 書き出しファイルの場所


#  テキストファイル書き出し
def mktxt_lists(txt, sitename):
    now = datetime.datetime.now()  # 本日の時間
    filename = export_file_path + now.strftime('%y%m%d') + '_' + sitename + '.txt'  # ファイル名作成

    try:  # データをCSVファイルに書き出す
        f = open(filename, 'w', encoding='ansi')
        f.writelines(txt)
        print(filename + '書き出し完了')
        f.close()
        return filename

    except UnicodeError as e:
        print(e)


#  二重配列CSV書き出し
def mkcsv_lists(data_list, sitename, encoding_type):
    now = datetime.datetime.now()  # 本日の時間
    filename = export_file_path + now.strftime('%y%m%d') + '_' + sitename + '.csv'  # ファイル名作成
    # データをCSVファイルに書き出す
    with open(filename, 'w', encoding=encoding_type, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_list)
    print(filename + '処理完了')


#  辞書CSV書き出し
def mkcsv_dir(dir_arr, labels, sitename):
    now = datetime.datetime.now()
    filename = export_file_path + now.strftime('%y%m%d') + '_' + sitename + '.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        for elem in dir_arr:
            writer.writerow(elem)
    print(filename + '処理完了')
    f.close()