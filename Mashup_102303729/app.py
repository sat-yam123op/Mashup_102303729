from flask import Flask, request
import zipfile
import os
import yagmail
from mashup import run_mashup

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            singer = (request.form.get("singer") or "").strip()
            email = (request.form.get("email") or "").strip()

            if not singer or not email:
                return "Singer and email are required"

            try:
                videos = int(request.form.get("videos", ""))
                duration = int(request.form.get("duration", ""))
            except ValueError:
                return "Videos and duration must be numbers"

            if videos <= 10 or duration <= 20:
                return "Videos must be >10 and duration >20 sec"

            output_file = "web_output.mp3"

            # generate mashup
            run_mashup(singer, videos, duration, output_file)

            # zip result
            zip_name = "result.zip"
            with zipfile.ZipFile(zip_name, "w") as z:
                z.write(output_file)

            # send email
            yag = yagmail.SMTP(
                os.environ.get("email_user"),
                os.environ.get("email_pass")
            )

            yag.send(
                to=email,
                subject="Your Mashup File",
                contents="Mashup generated successfully!",
                attachments=zip_name
            )

            return "✅ Mashup created and emailed!"

        except Exception as e:
            return f"Error: {e}"

    return """
<h2>Mashup Generator — 102303729</h2>
<form method="post">
    Singer: <input name="singer"><br><br>
    Videos (>10): <input name="videos"><br><br>
    Duration sec (>20): <input name="duration"><br><br>
    Email: <input name="email"><br><br>
    <input type="submit">
</form>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)