import { messageStore, socket, type WS } from "$lib/stores";

let queue: (string | ArrayBufferLike | Blob | ArrayBufferView)[] = [];

export function initWebSocket() {
    let wsUrl = "";

    if (window.location.protocol === "http:") {
        wsUrl = "ws://";
    } else {
        wsUrl = "wss://";
    }

    wsUrl += window.location.host + "/api/ws/";

    const websocket = new WebSocket(wsUrl) as WS;

    websocket.sendQueued = (data: string | ArrayBufferLike | Blob | ArrayBufferView) => {
        if (websocket.readyState === 1) {
            websocket.send(data);
        } else {
            queue.push(data);
        }
    };

    websocket.onopen = () => {
        queue.forEach((data) => websocket.send(data));
        queue = [];
    };

    const reConnect = () => {
        if (websocket.readyState !== WebSocket.OPEN) {
            socket.set(null);
            initWebSocket();
        }
    };

    websocket.onclose = () => reConnect();
    websocket.onmessage = handleWsMessage;

    socket.set(websocket as WS);

    return websocket;
}

function handleWsMessage(event: MessageEvent) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const payload: { e: string; d: any } = JSON.parse(event.data);

    switch (payload.e) {
        case "MESSAGE_CREATE":
            messageStore.update((msgs) => {
                if (msgs[payload.d.channel]) {
                    msgs[payload.d.channel].count++;

                    // Add the new message to the start of the array
                    msgs[payload.d.channel].results?.unshift(payload.d);
                }

                return msgs;
            });
            break;

        case "MESSAGE_DELETE":
        case "MESSAGE_UPDATE":
        case "CHANNEL_CREATE":
        case "CHANNEL_DELETE":
        case "CHANNEL_UPDATE":
        case "MEMBER_JOIN":
        case "MEMBER_UPDATE":
        case "MEMBER_LEAVE":
    }
}
