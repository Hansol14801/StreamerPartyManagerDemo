# Streamer Party Manager Demo

Public simulation build of **Streamer Party Manager**.

This repository is provided so the participation-management flow can be tested without CHZZK developer credentials, a CHZZK account, a Riot API key, or a running League of Legends client.

> **Demo safety:** This build does not connect to CHZZK and does not send requests to the League Client API (LCU). Chat messages, lobby members, invitations, removals, game phases, and game-count changes are simulated locally.

## Quick start

1. Run `1_install.cmd` once.
2. Run `2_start_demo.cmd`.
3. The demo page opens automatically at `http://127.0.0.1:8787`.
4. Enter a simulated command such as `!시참 TestPlayer#KR1`.
5. Use the demo controls to simulate invitations, game progress, rotation counts, and participant removal.

## What can be tested

- Simulated `!시참 GameName#TAG` chat participation
- Participation queue
- Simulated five-player League lobby
- Individual and empty-slot invitations
- Simulated game completion and participation-count tracking
- Two-game rotation display
- Participant removal
- Local-only reset of demo state

## Production integration represented by this demo

The private production build integrates CHZZK for incoming participation messages and uses the League Client API locally for lobby management. The production integration uses the following LCU operations:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/lol-lobby/v2/lobby` | Read current lobby and members |
| `GET` | `/lol-gameflow/v1/gameflow-phase` | Read game-flow state for participation tracking |
| `POST` | `/lol-lobby/v2/lobby/invitations` | Invite a viewer selected by the streamer |
| `DELETE` | `/lol-lobby/v2/lobby/members/{summonerId}` | Remove a participant when manually requested |

**None of these LCU endpoints are called by this public Demo repository.**

## 한국어

이 저장소는 Streamer Party Manager의 **공개 테스트 전용 Demo 버전**입니다.

치지직 개발자 앱/계정, Riot API Key, League of Legends 클라이언트 없이도 시참 관리 흐름을 확인할 수 있습니다. Demo에서는 치지직 채팅, LoL 로비, 초대/내보내기, 게임 진행 상태를 모두 로컬에서 가상으로 처리합니다.

실제 방송용 버전의 인증 정보나 실제 CHZZK/LCU 연결 기능은 이 저장소에 포함하지 않습니다.

### 파일

- `demo.py` — 로컬 시뮬레이션 서버
- `templates/demo.html` — Demo 관리자 화면
- `static/style.css` — 화면 스타일
- `1_install.cmd` — 최초 설치
- `2_start_demo.cmd` — Demo 실행
- `requirements.txt` — Python 의존성

---

## Riot Games Legal Notice

> Streamer Party Manager isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
