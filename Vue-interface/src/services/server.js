import http from '../utils/http.js';

export function addServer(data) {
    return http.post('http://localhost:8000/servers/create/', data);
}

export function getServer(serverName) {
    const params = { name: serverName };
    return http.get(`http://localhost:8000/servers/get/`, { params });
}

export function getAllServers() {
    return http.get('http://localhost:8000/servers/list/');
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
export function getServerAttrPer(server_name, attribute, period, spacing) {
    const params = { server_name, attribute, period, spacing };
    return http.get('http://localhost:8000/servers/data/', { params });
}

export function activateServer(server) {
    return http.put('http://localhost:8000/servers/activation/', { name: server });
}

export function deleteServer(server) {
    return http.delete(`http://localhost:8000/servers/delete/${server}/`);
}
