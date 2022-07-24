import packages from "../../package.json"

class OSAccounts {
    static isLogged = localStorage.getItem('session_json') != null ? true : false
    static request(method, data) {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify(data);

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        return fetch(`${packages.config.request_url}/api/${method}`, requestOptions)
    }
}

export default OSAccounts