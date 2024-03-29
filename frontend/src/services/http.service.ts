import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

const decamelizeRequest = (config: AxiosRequestConfig) => {
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
    (response.headers["Content-Type"] === "application/json" ||
      response.headers["content-type"] === "application/json")
  ) {
    response.data = camelizeKeys(response.data);
  }
  return response;
};

const client = axios.create();

client.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    return decamelizeRequest(config);
  },
  (err) => {
    return Promise.reject(decamelizeRequest(err));
  }
);

client.interceptors.response.use(
  (response: AxiosResponse) => {
    return camelizeResponse(response);
  },
  (err) => {
    return Promise.reject(camelizeResponse(err));
  }
);

export { client };
