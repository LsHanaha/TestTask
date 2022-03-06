import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://0.0.0.0:8888/api"
})


export const storeToken = (token) => {
  localStorage.removeItem("token");
  localStorage.setItem("token", token);
}


export const getToken = () => {
  const token = localStorage.getItem("token");
  if (token) {
    return { Authorization: 'Bearer ' + token }
  }
  return "";
}


export const getQueries = async (endpoint) => {
  const config = {headers: getToken()}

  try {
    return await axiosInstance.get(endpoint, config);
  } catch (error) {
    throw new Error(JSON.stringify(error.response.data.detail));
  }
};

export const postQueries = async (endpoint, postParams) => {
  try {
    const response = await axiosInstance.post(endpoint, postParams, { headers: getToken() });
    return response;
  } catch (error) {
    throw new Error(JSON.stringify(error.response?.data?.detail || error.response?.data));
  }
};

export const updateQueries = async (endpoint, putParams) => {
  try {
    return await axiosInstance.put(
      endpoint,
      putParams,
      {headers: getToken()}
    );

  } catch (error) {
    throw new Error(JSON.stringify(error.response?.data?.detail || error.response?.data));
  }
};

export const deleteQueries = async (endpoint) => {
  const config = { headers: getToken() };

  try {
    return await axiosInstance.delete(endpoint, config);
  } catch (error) {
    throw new Error(JSON.stringify(error.response?.data?.detail || error.response?.data));
  }
};

