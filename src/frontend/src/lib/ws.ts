import { page } from "$app/stores";
import { joinedTopicRooms, joinedTopics, messageStore, socket, type WS } from "$lib/stores";
import { get } from "svelte/store";
import type {
    TopicChatChannelInterface,
    TopicChatMessageInterface,
    TopicChatRoomInterface,
    UserInterface
} from "./types";
import { goto } from "$app/navigation";

let queue: (string | ArrayBufferLike | Blob | ArrayBufferView)[] = [];

interface WSInitOptions {
    reconnecting?: boolean;
}

export function initWebSocket(options: WSInitOptions = {}) {
    let wsUrl = "";

    if (window.location.protocol === "http:") {
        wsUrl = "ws://";
    } else {
        wsUrl = "wss://";
    }

    wsUrl += window.location.host + "/api/ws/";

    if (options.reconnecting) {
        wsUrl += "?reconnect=true";
    }

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
            initWebSocket({ reconnecting: true });
        }
    };

    websocket.onclose = () => reConnect();
    websocket.onmessage = handleWsMessage;

    socket.set(websocket as WS);

    return websocket;
}

function handleWsMessage(event: MessageEvent) {
    const payload: // e: event name, d: data
    | { e: "MESSAGE_CREATE"; d: TopicChatMessageInterface }
        | { e: "MESSAGE_DELETE"; d: { id: number; channel_id: number } }
        | { e: "MESSAGE_UPDATE"; d: TopicChatMessageInterface }
        | { e: "CHANNEL_CREATE"; d: TopicChatChannelInterface }
        | { e: "CHANNEL_UPDATE"; d: TopicChatChannelInterface }
        | { e: "CHANNEL_DELETE"; d: { id: number; topic: string } }
        | { e: "TOPIC_ROOM_UPDATE"; d: TopicChatRoomInterface }
        | { e: "ROOM_MEMBER_JOIN"; d: { user: UserInterface; room: TopicChatRoomInterface } }
        | { e: "ROOM_MEMBER_UPDATE"; d: unknown }
        | { e: "ROOM_MEMBER_LEAVE"; d: unknown } = JSON.parse(event.data);

    console.log(`Received event ${payload.e}`);

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
            break;

        case "MESSAGE_UPDATE":
            break;

        case "CHANNEL_CREATE":
            joinedTopics.update((topics) => {
                payload.d as TopicChatChannelInterface;
                topics[payload.d.topic].channels = [...topics[payload.d.topic].channels, payload.d];

                return topics;
            });
            break;

        case "CHANNEL_DELETE":
            joinedTopics.update((topics) => {
                topics[payload.d.topic].channels = topics[payload.d.topic]!.channels.filter(
                    (channel) => channel.id !== payload.d.id
                );

                return topics;
            });

            messageStore.update((msgs) => {
                delete msgs[payload.d.id];
                return msgs;
            });

            if (parseInt(get(page).params.channel_id) === payload.d.id) {
                // Redirect the user if he is currently viewing that channel
                goto(`/topics/${payload.d.topic}/channel/`);
            }
            break;

        case "CHANNEL_UPDATE":
            break;

        case "ROOM_MEMBER_JOIN": {
            const joinedRoom = payload.d.room;

            joinedTopicRooms.update((joinedRooms) => {
                if (joinedRooms[joinedRoom.topic]) {
                    console.log(1);
                    const roomIndex = joinedRooms[joinedRoom.topic].findIndex(
                        (room) => room.id === joinedRoom.id
                    );

                    if (roomIndex) {
                        console.log(2, roomIndex, joinedRooms[joinedRoom.topic][roomIndex]);
                        joinedRooms[joinedRoom.topic][roomIndex] = joinedRoom;
                        console.log(2.5, roomIndex, joinedRooms[joinedRoom.topic][roomIndex]);
                    } else {
                        console.log(3);
                        // use joined a new room
                        joinedRooms[joinedRoom.topic].push(joinedRoom);
                        goto(`/topics/${joinedRoom.topic}/channel/${joinedRoom.id}/`);
                    }
                } else {
                    console.log(4);
                    joinedRooms[joinedRoom.topic] = [joinedRoom];
                    goto(`/topics/${joinedRoom.topic}/channel/${joinedRoom.id}/`);
                }

                console.log(5);
                return joinedRooms;
            });

            break;
        }

        case "ROOM_MEMBER_UPDATE":
        case "ROOM_MEMBER_LEAVE":
        case "TOPIC_ROOM_UPDATE":
    }
}
