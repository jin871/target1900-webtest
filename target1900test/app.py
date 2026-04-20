from flask import Flask, render_template, request, jsonify
import csv
import random
import os

app = Flask(__name__)

# CSV読み込み関数
def load_words(filename):
    words = []
    if not os.path.exists(filename): return []
    try:
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader, None) # ヘッダーを飛ばす
            for row in reader:
                if len(row) >= 3:
                    words.append({
                        'Number': row[0].strip(),
                        'English': row[1].strip(),
                        'Japanese': row[2].strip()
                    })
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return words

@app.route('/')
def index():
    return render_template('index.html')

# 問題データを送る処理（通常モードのみサーバーが行う）
@app.route('/get_words', methods=['POST'])
def get_words():
    data = request.json
    question_count = int(data.get('count', 10))
    ranges = data.get('ranges', [[1, 1900]]) 
    
    all_words = load_words('target1900.csv')
    
    if not all_words:
        return jsonify({"error": "データが見つかりません。target1900.csvを確認してください。"})
        
    filtered_words = []
    for w in all_words:
        try:
            num = int(w['Number'])
            in_range = False
            for r_start, r_end in ranges:
                if r_start <= num <= r_end:
                    in_range = True
                    break
            if in_range:
                filtered_words.append(w)
        except ValueError:
            continue
    
    if not filtered_words:
        return jsonify({"error": "選択された範囲に単語がありません。範囲指定を確認してください。"})
        
    sample_size = min(question_count, len(filtered_words))
    words = random.sample(filtered_words, sample_size)
    
    return jsonify({"words": words})

if __name__ == '__main__':
    app.run(debug=True)
