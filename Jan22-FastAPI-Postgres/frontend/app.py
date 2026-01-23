from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "some_random_secret_key"  # Required for flashing messages

# The URL of your running FastAPI backend
FASTAPI_URL = "http://127.0.0.1:8000/users/"

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 1. Get data from the HTML form
        form_data = {
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone_number": request.form.get("phone_number")
        }

        # 2. Send data to FastAPI (mimicking Postman)
        try:
            response = requests.post(FASTAPI_URL, json=form_data)
            
            if response.status_code == 200:
                flash("Success! User created in Database.", "success")
            else:
                # Extract error message from FastAPI response
                error_detail = response.json().get("detail", "Unknown Error")
                flash(f"Error: {error_detail}", "danger")
                
        except requests.exceptions.ConnectionError:
            flash("Error: Could not connect to backend. Is FastAPI running?", "danger")

        return redirect(url_for("register"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)