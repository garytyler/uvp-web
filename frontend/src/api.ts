import axios from "axios";
import applyConverters from "axios-case-converter";
import {
  IUserProfile,
  IUserProfileCreate,
  IUserProfileUpdate,
  IGuest,
  IGuestCreate,
  IGuestUpdate,
} from "@/interfaces";
import { IFeature } from "@/interfaces";
import { apiUrl } from "@/env";

const client = applyConverters(axios.create());

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

const accountsApi = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);
    return axios.post(`${apiUrl}/api/access/token`, params);
  },
  async getCurrentUser(token: string) {
    return axios.get<IUserProfile>(
      `${apiUrl}/api/users/current`,
      authHeaders(token)
    );
  },
  async updateCurrentUser(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/users/current`,
      data,
      authHeaders(token)
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/users`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    console.log(apiUrl);
    return axios.post(`${apiUrl}/api/users`, data);
  },
  async passwordRecovery(email: string) {
    return axios.post(
      `${apiUrl}/api/access/request-password-recovery/${email}`
    );
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/access/reset-password`, {
      newPassword: password,
      token,
    });
  },
};

const guestsApi = {
  async getCurrentGuest() {
    const path = `${apiUrl}/api/guests/current`;
    return client.get<IGuest>(path);
  },
  async getGuest(guestId: string) {
    const path = `${apiUrl}/api/guests/${guestId}`;
    return client.get<IGuest>(path);
  },
  async createCurrentGuest(data: IGuestCreate) {
    const path = `${apiUrl}/api/guests/current`;
    return client.post(path, data);
  },
  async updateGuest(guestId: string, data: IGuestUpdate) {
    const path = `${apiUrl}/api/guests/${guestId}`;
    return client.patch(path, data);
  },
  async deleteGuest(featureId: string, guestId: string) {
    const path = `${apiUrl}/api/features/${featureId}/guests/${guestId}`;
    return client.delete(path);
  },
};

const featuresApi = {
  async getFeature(slugOrId: string) {
    const path = `${apiUrl}/api/features/${slugOrId}`;
    return client.get<IFeature>(path);
  },
};

export const api = {
  ...accountsApi,
  ...guestsApi,
  ...featuresApi,
};
