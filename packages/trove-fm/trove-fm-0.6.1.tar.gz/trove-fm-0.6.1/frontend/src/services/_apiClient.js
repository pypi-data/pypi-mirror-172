
import axios from 'axios';

export const apiClient = axios.create({
    baseURL: 'https://trove.boathouse/api',
    rejectUnauthorized: false,
})

export const registerPerson = (new_creds) => apiClient.post('/person/', new_creds).then(
    function (response) {
        console.log("RESPONSE: ")
        console.log(response.data)
        return response
    }
).catch(
    function (error) {
        console.log("LOGGING THE ERROR...")
        console.log(error.response.data.detail)
        return error
    }
)

export const loginPerson = () => apiClient.post('/person/login/token/')

export const getPerson = () => apiClient.get('/person/profile/')

export const getPing = () => apiClient.get('/ping/').then(res => res.data)
