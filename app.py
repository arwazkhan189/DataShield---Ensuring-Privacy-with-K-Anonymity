from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io

app = Flask(__name__)

# Simple k-anonymity function
def apply_k_anonymity(df, k, columns):
    for col in columns:
        df[col] = df[col].astype(str).apply(lambda x: x[:len(x)-k] + '*'*k if len(x) > k else '*'*len(x))
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Get form values
        k = int(request.form['k_value'])
        columns = request.form['columns'].replace(" ", "").split(",")

        # Read the uploaded file into a DataFrame
        df = pd.read_csv(file)
        df_anonymized = apply_k_anonymity(df, k, columns)

        # Convert DataFrame to CSV (in memory, no saving)
        output = io.StringIO()
        df_anonymized.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode()), 
            as_attachment=True,
            mimetype="text/csv",
            download_name=f"anonymized_{file.filename}"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)