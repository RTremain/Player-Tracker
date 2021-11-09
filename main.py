from datetime import datetime
import database.db_management, database.seedDB, database.createDB
from flask import Flask, jsonify, request

database.createDB.create_database()

database.seedDB.seed_database()


app = Flask(__name__)


@app.route('/api')
def index():
    return {"success": True}, 200

@app.route('/api/player')
def get_player():
    playerName = request.args.get('playerName')
    server = request.args.get('server')
    
    if playerName == None or playerName == "" or server == None or server == "":
        return { "error": "Missing Tags"}, 400
        
    player = database.db_management.get_player(str(playerName), str(server))
    return jsonify(player), 200

@app.route('/api/rank')
def get_rank():
    rankName = request.args.get('rankName')
    rank = database.db_management.get_player_rank(str(rankName))
    return jsonify(rank), 200

@app.route('/api/player/server/<id>')
def get_player_server(id):


    player = database.db_management.get_player_by_id(id)

    server = database.db_management.get_server(player)

    return server, 200

@app.route('/api/player/reports/<id>')
def get_player_reports(id):
    return jsonify(database.db_management.get_reports(id)), 200


@app.route('/api/player/commendations/<id>')
def get_player_commendations(id):
    return jsonify(database.db_management.get_commendations(id)), 200


@app.route('/api/reports', methods = ['POST', 'GET'])
def handle_report():
    if request.method == 'POST':
        data = request.form
        print(data.get('reportedBy'))
        reportedBy = data.get('reportedBy')
        reporterDiscordId = data.get('reporterId')
        reportedBy = data.get('reportedBy')
        reporterId = database.db_management.get_user(reportedBy, reporterDiscordId).get('id')
        reportedName = data.get('reportedName')
        server = data.get('server')
        reportedId = database.db_management.get_player(reportedName, server).get('id')
        reportedCause = data.get('cause')
        commendationStatus = data.get('commendation')
        timeOfReport = datetime.now()


        
        report = [reporterId, reportedId, reportedName, reportedCause, commendationStatus, timeOfReport]

        print(report)

        database.db_management.create_report(report)

        return {"Success: ": "Report Created Successfully"}, 200

    elif request.method == 'GET':
        reportId = request.args.get('reportId')
        report = database.db_management.get_report_by_id(reportId)
        return jsonify(report)



if __name__ == "__main__":
    app.run(debug=True)