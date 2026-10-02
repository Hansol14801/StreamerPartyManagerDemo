from flask import Flask, jsonify, render_template, request
import re
import threading
import webbrowser

app = Flask(__name__)

CAPACITY = 5
state = {
    "phase": "Lobby",
    "queue": [],
    "lobby": [{"riot_id": "Streamer#DEMO", "name": "Streamer (Host)", "games": 0, "host": True}],
    "history": [],
    "next_id": 1,
    "rotation_games": 2,
}

def valid_riot_id(value):
    return bool(re.match(r"^.{1,32}#[^#\s]{1,10}$", (value or "").strip()))

def snapshot():
    return {
        "demo": True,
        "phase": state["phase"],
        "capacity": CAPACITY,
        "rotation_games": state["rotation_games"],
        "queue": state["queue"],
        "lobby": state["lobby"],
        "history": state["history"],
    }

@app.get("/")
def index():
    return render_template("demo.html")

@app.get("/api/state")
def api_state():
    return jsonify(snapshot())

@app.post("/api/settings/rotation")
def set_rotation():
    data = request.get_json(force=True) or {}
    try:
        games = int(data.get("rotation_games", 2))
    except (TypeError, ValueError):
        return jsonify(ok=False, message="로테이션 판수는 숫자로 입력해주세요."), 400
    if games < 1 or games > 10:
        return jsonify(ok=False, message="로테이션 판수는 1~10판으로 설정해주세요."), 400
    state["rotation_games"] = games
    return jsonify(ok=True, message=f"로테이션 기준을 {games}판으로 변경했습니다.")

@app.post("/api/chat")
def chat():
    data = request.get_json(force=True)
    name = (data.get("name") or "DemoViewer").strip()
    content = (data.get("content") or "").strip()
    match = re.match(r"^!시참\s+(.+?#\S+)\s*$", content, re.I)
    if not match or not valid_riot_id(match.group(1)):
        return jsonify(ok=False, message="!시참 GameName#TAG 형식으로 입력해주세요."), 400

    riot_id = match.group(1).strip()
    all_ids = [x["riot_id"].lower() for x in state["queue"] + state["lobby"]]
    if riot_id.lower() in all_ids:
        return jsonify(ok=False, message="이미 대기열 또는 로비에 있는 Riot ID입니다."), 409

    state["queue"].append({
        "id": state["next_id"],
        "riot_id": riot_id,
        "name": name,
        "games": 0,
    })
    state["next_id"] += 1
    return jsonify(ok=True, message="가상 치지직 채팅으로 대기열에 등록했습니다.")

@app.post("/api/invite/<int:queue_id>")
def invite(queue_id):
    if len(state["lobby"]) >= CAPACITY:
        return jsonify(ok=False, message="가상 로비가 가득 찼습니다."), 400
    viewer = next((x for x in state["queue"] if x["id"] == queue_id), None)
    if not viewer:
        return jsonify(ok=False, message="대기자를 찾을 수 없습니다."), 404
    state["queue"].remove(viewer)
    state["lobby"].append({**viewer, "host": False})
    return jsonify(ok=True, message=f'{viewer["riot_id"]} 초대를 시뮬레이션했습니다.')

@app.post("/api/invite-empty")
def invite_empty():
    invited = []
    while state["queue"] and len(state["lobby"]) < CAPACITY:
        viewer = state["queue"].pop(0)
        state["lobby"].append({**viewer, "host": False})
        invited.append(viewer["riot_id"])
    return jsonify(ok=True, invited=invited, message=f"{len(invited)}명을 가상 로비에 추가했습니다.")

@app.post("/api/kick/<int:queue_id>")
def kick(queue_id):
    viewer = next((x for x in state["lobby"] if not x.get("host") and x.get("id") == queue_id), None)
    if not viewer:
        return jsonify(ok=False, message="참가자를 찾을 수 없습니다."), 404
    state["lobby"].remove(viewer)
    state["history"].append({**viewer, "result": "removed"})
    return jsonify(ok=True, message=f'{viewer["riot_id"]} 내보내기를 시뮬레이션했습니다.')

@app.post("/api/complete-game")
def complete_game():
    state["phase"] = "EndOfGame"
    for viewer in state["lobby"]:
        if not viewer.get("host"):
            viewer["games"] = viewer.get("games", 0) + 1
    state["phase"] = "Lobby"
    return jsonify(ok=True, message="가상 게임 1판을 완료했습니다. 참가자의 판수가 증가했습니다.")

@app.post("/api/reset")
def reset():
    state["phase"] = "Lobby"
    state["queue"].clear()
    state["lobby"][:] = [{"riot_id": "Streamer#DEMO", "name": "Streamer (Host)", "games": 0, "host": True}]
    state["history"].clear()
    state["next_id"] = 1
    return jsonify(ok=True, message="Demo 상태를 초기화했습니다.")

if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8787")).start()
    app.run("127.0.0.1", 8787, debug=False, threaded=True)
