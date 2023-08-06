
import axios from "axios"
import { formatURL } from "../utils/urls"

const getClient = () => {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
    }
  }
  console.log('GETTING CLIENT')

  return {
    get: (url, data, options = {}) => axios.get(url, { ...defaultOptions, ...options }),
    post: (url, data, options = {}) => axios.post(url, data, { ...defaultOptions, ...options }),
    put: (url, data, options = {}) => axios.put(url, data, { ...defaultOptions, ...options }),
    delete: (url, data, options = {}) => axios.delete(url, { ...defaultOptions, ...options })
  }
}

/**
 *
 * @param {String} url - relative api endpoint url
 * @param {String} method - "GET", "POST", "PUT", "DELETE"
 * @param {Object} types - object with three keys representing the different action types: REQUEST, SUCCESS, FAILURE
 * @param {Object} options - object with potential data and query params
 * @param {Function} onSuccess - callback to run with the returned data, if any
 * @param {Function} onFailure - callback to run with the returned error, if any
 */
const apiClient = ({
  url,
  method,
  options: { data, params },
  onSuccess = (res) => ({ type: res.type, success: true, status: res.status, data: res.data }),
  onFailure = (res) => ({ type: res.type, success: false, status: res.status, error: res.error })
}) => {
  console.log('HERE IN API CLIENT')
  return async () => {
    const client = getClient()
    const urlPath = formatURL(url, params)

    try {
      const res = await client[method.toLowerCase()](urlPath, data)
      console.log("URL PATH: " + urlPath)
      console.log(res)
      return onSuccess({ type: 'SUCCESS', ...res })
    } catch (error) {
      console.log(error)
      return onFailure({ type: 'FAILURE', status: error.status, error: error.response })
    }
  }
}

export default apiClient
