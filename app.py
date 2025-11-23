from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    op = data.get('operation')
    matrices = data.get('matrices', [])
    results = []

    try:
        if op == 'multiply':
            if len(matrices) != 2:
                return jsonify(error="Matris çarpımı için 2 matris gereklidir!")
            A, B = np.array(matrices[0]), np.array(matrices[1])
            if A.shape[1] != B.shape[0]:
                return jsonify(error="A'nın sütun sayısı, B'nin satır sayısına eşit olmalı!")
            C = A @ B
            results.append(C.round(3).tolist())

        elif op == 'transpose':
            if len(matrices) < 1:
                return jsonify(error="Transpoze işlemi için bir matris oluşturun!")
            for m in matrices:
                arr = np.array(m)
                results.append(arr.T.round(3).tolist())

        elif op == 'determinant':
            if len(matrices) < 1:
                return jsonify(error="Determinant işlemi için bir matris oluşturun!")
            for m in matrices:
                arr = np.array(m)
                if arr.shape[0] != arr.shape[1]:
                    results.append("Kare matris değil!")
                else:
                    results.append(float(np.round(np.linalg.det(arr), 3)))

        elif op == 'inverse':
            if len(matrices) < 1:
                return jsonify(error="Ters alma işlemi için bir matris oluşturun!")
            for m in matrices:
                arr = np.array(m)
                if arr.shape[0] != arr.shape[1]:
                    results.append("Kare matris değil!")
                elif np.linalg.det(arr) == 0:
                    results.append("Det=0 → Ters yok")
                else:
                    inv = np.linalg.inv(arr)
                    results.append(inv.round(3).tolist())

        return jsonify(results=results)

    except Exception as e:
        return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
