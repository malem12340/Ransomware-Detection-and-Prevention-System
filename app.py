from flask import Flask, render_template, session, redirect, url_for, jsonify

from config import Config

from modules.auth import auth
from modules.monitoring import start_monitoring
from modules.dashboard import Dashboard
from modules.restore import RestoreManager


app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY


# ----------------------------------------
# Start Monitoring Automatically
# ----------------------------------------

observer = start_monitoring()


# ----------------------------------------
# Register Blueprints
# ----------------------------------------

app.register_blueprint(auth)


# ----------------------------------------
# Manager Objects
# ----------------------------------------

dashboard_manager = Dashboard()
restore_manager = RestoreManager()


# ----------------------------------------
# Dashboard
# ----------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = dashboard_manager.get_dashboard_data()

    return render_template(
        "dashboard.html",
        username=session["username"],
        monitored=0,
        rapid_changes=0,
        alerts=data["alerts"],
        logs=data["logs"],
        backups=data["backups"],
        recent_logs=data["recent_logs"],
        recent_alerts=data["recent_alerts"],
        system_status=data["system_status"],
        chart_data=data["chart_data"]
    )


# ----------------------------------------
# Dashboard API
# ----------------------------------------

@app.route("/dashboard-data")
def dashboard_data():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = dashboard_manager.get_dashboard_data()

    return jsonify({

        "alerts": data["alerts"],

        "logs": data["logs"],

        "backups": data["backups"],

        "recent_logs": data["recent_logs"],

        "recent_alerts": data["recent_alerts"],

        "system_status": data["system_status"]

    })


# ----------------------------------------
# Application Start
# ----------------------------------------

if __name__ == "__main__":

    try:

        app.run(debug=True)

    finally:

        observer.stop()
        observer.join()