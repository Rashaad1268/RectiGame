import { json } from "@sveltejs/kit";


export async function GET({ request, cookies, url }) {
    if (cookies.get('sessionid') == undefined) {
        return json({wsUrl: null, sessionIdExists: false})
    }

    let wsAddr: string | undefined = process.env.SERVER_ADDR;
    const wsQueryParam = `?authorization=${cookies.get('sessionid')}`

    if (wsAddr) {
        wsAddr = wsAddr.replace("http://", "");
        wsAddr = wsAddr.replace("https://", "");

        wsAddr = `ws://${wsAddr}api/ws/${wsQueryParam}`
    } else {
        wsAddr = `ws://${url.host}/api/ws/${wsQueryParam}`
    }

    return json({wsUrl: wsAddr, sessionIdExists: true})
}