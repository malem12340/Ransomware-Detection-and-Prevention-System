from flask import Flask, render_template, session, redirect, url_for, jsonify

from config import Config

from modules.auth import auth
from modules.monitoring import start_monitoring
from modules.dashboard import Dashboard
from modules.restore import RestoreManager


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY


# ==========================================
# START FILE MONITORING
# ==========================================

observer = start_monitoring()


# ==========================================
# REGISTER BLUEPRINT
# ==========================================

app.register_blueprint(auth)


# ==========================================
# MANAGERS
# ==========================================

dashboard_manager = Dashboard()
restore_manager = RestoreManager()


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = dashboard_manager.get_dashboard_data()

    return render_template(
        "dashboard.html",

        username=session["username"],

        monitored=data["monitored"],

        rapid_changes=data["rapid_changes"],

        alerts=data["alerts"],

        logs=data["logs"],

        backups=data["backups"],

        recent_logs=data["recent_logs"],

        recent_alerts=data["recent_alerts"],

        system_status=data["system_status"],

        chart_data=data["chart_data"]
    )


# ==========================================
# DASHBOARD DATA API
# ==========================================

@app.route("/dashboard-data")
def dashboard_data():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = dashboard_manager.get_dashboard_data()

    return jsonify({

        "monitored": data["monitored"],

        "rapid_changes": data["rapid_changes"],

        "alerts": data["alerts"],

        "logs": data["logs"],

        "backups": data["backups"],

        "recent_logs": data["recent_logs"],

        "recent_alerts": data["recent_alerts"],

        "system_status": data["system_status"],

        "chart_data": data["chart_data"]
    })


# ==========================================
# ALERTS PAGE
# ==========================================

@app.route("/alerts")
def alerts():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from db import Database

    db = Database()

    query = """
        SELECT
            alert_type,
            severity,
            description,
            alert_time
        FROM alerts
        ORDER BY alert_time DESC
        LIMIT 50
    """

    db.execute(query)

    alerts_data = db.fetchall()

    db.close()

    return render_template(
        "alerts.html",
        username=session["username"],
        alerts=alerts_data
    )


# ==========================================
# LOGS PAGE
# ==========================================

@app.route("/logs")
def logs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from db import Database

    db = Database()

    query = """
        SELECT
            username,
            action,
            log_time
        FROM logs
        ORDER BY log_time DESC
        LIMIT 50
    """

    db.execute(query)

    logs_data = db.fetchall()

    db.close()

    return render_template(
        "logs.html",
        username=session["username"],
        logs=logs_data
    )


# ==========================================
# SETTINGS PAGE
# ==========================================

@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "settings.html",
        username=session["username"]
    )


# ==========================================
# FILE MONITORING PAGE
# ==========================================

@app.route("/file-monitoring")
def file_monitoring():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from db import Database

    db = Database()

    query = """
        SELECT
            file_path,
            event_type,
            event_time,
            status
        FROM file_events
        ORDER BY event_time DESC
        LIMIT 100
    """

    db.execute(query)

    file_events = db.fetchall()

    db.close()

    return render_template(
        "file_monitoring.html",
        username=session["username"],
        file_events=file_events
    )


# ==========================================
# BACKUP PAGE
# ==========================================

@app.route("/backup")
def backup():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from db import Database

    db = Database()

    query = """
        SELECT
            file_name,
            original_path,
            backup_path,
            backup_time
        FROM backup_history
        ORDER BY backup_time DESC
        LIMIT 100
    """

    db.execute(query)

    backups_data = db.fetchall()

    db.close()

    return render_template(
        "backup.html",
        username=session["username"],
        backups=backups_data
    )


# ==========================================
# LOGOUT IS HANDLED BY AUTH BLUEPRINT
# ==========================================

# ==========================================
# CHECK REGISTERED ROUTES
# ==========================================

print("\n========== REGISTERED ROUTES ==========")

for rule in app.url_map.iter_rules():
    print(rule, "->", rule.endpoint)

print("=======================================\n")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    try:

        app.run(
            debug=True,
            use_reloader=False
        )

    finally:

        observer.stop()

        observer.join()