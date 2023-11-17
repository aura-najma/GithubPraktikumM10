import os, csv
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/") 
def hello_world(): 
    return render_template("welcome.html")  

@app.route("/cv_aura")
def look_cv(): 
    return render_template("cv_aura.html")

@app.route("/biodata_aura") 
def look_biodata(): 
    return render_template("biodata_aura.html")

@app.route("/portofolio_aura")
def look_portofolio():
    return render_template("portofolio_aura.html")

@app.route("/daftarmatkultsd")
def look_daftarmatkul():
    return render_template("daftarmatkultsd.html")

@app.route("/artikelPTM_aura")
def look_artikelPTM():
    return render_template("artikelPTM.html")

@app.route("/fibonacci", methods=["GET", "POST"])
def fibonacci():
    if request.method == "POST":
        try:
            n = int(request.form["number"])
            fibonacci_sequence = generate_fibonacci(n)
            return render_template("fibonacci.html", n=n, sequence=fibonacci_sequence)
        except ValueError:
            return "Invalid input. Please enter a valid integer."
    
    return render_template("fibonacci_input.html")

def generate_fibonacci(n):
    sequence = [1, 1]
    while len(sequence) < n:
        next_num = sequence[-1] + sequence[-2]
        sequence.append(next_num)
    return sequence

@app.route("/csv_to_json", methods=["GET", "POST"])
def csv_to_json():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        allowed_extensions = {"csv"}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return "Invalid file type. Please upload a CSV file."

        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        json_data = convert_csv_to_json(file_path)

        return jsonify(json_data)

    return render_template("csv_to_json.html")

def convert_csv_to_json(file_path):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = [row for row in csv_reader]

    return json_data

@app.route("/order_submit", methods=["POST"])
def order_submit():
    name = request.form.get("name")
    quantity_bomboloni = int(request.form.get("quantity_bomboloni"))
    quantity_risol = int(request.form.get("quantity_risol"))
    amount_paid = int(request.form.get("amount_paid"))

    price_bomboloni = 5000
    price_risol = 4000
    total_price = (quantity_bomboloni * price_bomboloni) + (quantity_risol * price_risol)

    change = amount_paid - total_price

    return redirect(url_for("thank_you", name=name, change=change))

@app.route("/thank_you")
def thank_you():
    name = request.args.get("name")
    change = int(request.args.get("change"))

    if change < 0:
        message = f"Maaf {name}, uangmu kurang sebesar {abs(change)}."
    else:
        message = f"Terima kasih {name}, kembalianmu sebesar {change}."

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Terima Kasih</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    background-color: #ff858e;
                    color: #fff;
                    text-align: center;
                }}
                h1 {{
                    color: #fff; 
                    margin-bottom: 10px;
                }}
                
            </style>
        </head>
        <body>
            <h1>{message}</h1>
        </body>
        </html>
    """

    return html_content