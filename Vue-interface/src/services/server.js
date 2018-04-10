import http from '../utils/http.js';

export function addServer(data) {
    return http.post('http://localhost:8000/servers/new', data);
}

export function getServer(serverName) {
    return http.get(`http://localhost:8000/servers/${serverName}/`);
}

export function getAllServers() {
    return http.get('http://localhost:8000/servers/');
}

/*
@params: data: { order: order }
*/
export function getServersSorted(data) {
    return http.get('http://localhost:8000/servers/order/', data);
}

/*
@params: {
    server: String,
    attr: String,
    period: String,
}
*/
export function getServerAttrPer(server, attr, period) {
    return http.get(`http://localhost:8000/servers/${server}/${attr}/${period}`);
}

export function activateServer(server) {
    return http.put(`http://localhost:8000/servers/${server}/activation/`);
}

export function deleteServer(server) {
    return http.delete(`http://localhost:8000/servers/${server}/`);
}
