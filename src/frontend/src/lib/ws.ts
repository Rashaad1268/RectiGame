import { messageStore, socket } from "$lib/stores";
import { get } from "svelte/store";

export function initWebSocket() {
    let wsUrl = "";

    if (window.location.protocol === "http:") {
        wsUrl = "ws://";
    } else {
        wsUrl = "wss://";
    }

    wsUrl += window.location.host + "/api/ws/";

    
    const websocket = new WebSocket(wsUrl);
    
    const reConnect = () => {
        console.log("Trying to reconnect...")
        if (websocket.readyState !== WebSocket.OPEN) {
            socket.set(null);
            initWebSocket()
        }
    }

    websocket.onclose = () => reConnect();
    websocket.onmessage = handleWsMessage;

    socket.set(websocket);

    return websocket;
}

function handleWsMessage(event: MessageEvent) {
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
