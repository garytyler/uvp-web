import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

const decamelizeRequest = (config: AxiosRequestConfig) => {
  console.log(config.headers);
  if (config.headers["Content-Type"] !== "multipart/form-data") {
    if (config.params) {
      config.params = decamelizeKeys(config.params);
    }
    if (config.data) {
      config.data = decamelizeKeys(config.data);
    }
  }
  return config;
};

const camelizeResponse = (response: AxiosResponse) => {
  if (
    response.data &&
    response.headers["Content-Type"] === "application/json"
  ) {
    response.data = camelizeKeys(response.data);
  }
  return response;
};

const client = axios.create();

client.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // return config;
    return decamelizeRequest(config);
  },
  (err) => {
    console.log(err);
    return Promise.reject(err);
  }
);

client.interceptors.response.use(
  (response: AxiosResponse) => {
    // return response;
    return camelizeResponse(response);
  },
  (err) => {
    console.log(err);
    return Promise.reject(err);
  }
);

export { client };
