from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SOURCE_API = "https://cekidml.caliph.dev/api/validasi"

@app.route("/api/ml/check", methods=["GET"])
def check_ml():
    player_id = request.args.get("id")
    server_id = request.args.get("serverid")

    if not player_id or not server_id:
        return jsonify({
            "status": "error",
            "message": "Missing id or serverid"
        }), 400

    try:
        r = requests.get(SOURCE_API, params={
            "id": player_id,
            "serverid": server_id
        }, timeout=10)

        data = r.json()

        # Optional: customize response
        if data.get("status") == "success":
            return jsonify({
                "status": "success",
                "player": {
                    "nickname": data["result"]["nickname"],
                    "country": data["result"]["country"]
                },
                "source": "shensi-api"
            })

        return jsonify({
            "status": "failed",
            "message": "Invalid player ID"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "API unavailable"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
