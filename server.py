from flask import Flask, jsonify, render_template
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

app = Flask(__name__, template_folder="templates") 
CORS(app)

SERVICE_ACCOUNT_FILE = "/etc/secrets/conference-tally-app-06d6b71fe066.json"  
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
sheets_service = build("sheets", "v4", credentials=credentials)
SPREADSHEET_ID = "1wGmhVHlPwMSY7kUUbfy2dUd9n9Am8HwgHjlReEm5Gzk"

@app.route("/")
def serve_tally():
    return render_template("tally.html")

@app.route("/get-conf-data", methods=["GET"])
def get_conf_data():
    try:
        sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets_info = sheet_metadata.get("sheets", [])
        used_row_counts = {}

        for sheet in sheets_info:
            sheet_name = sheet["properties"]["title"]
            result = sheets_service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A2:A").execute()
            values = result.get("values", [])
            used_row_counts[sheet_name] = sum(1 for row in values if row and row[0].strip())

        return jsonify(used_row_counts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(debug=True, host="0.0.0.0", port=port)
