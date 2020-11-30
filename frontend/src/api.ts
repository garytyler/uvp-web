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
    return axios.post(`/api/login/access-token`, params);
  },
  async getCurrentUser(token: string) {
    return axios.get<IUserProfile>(`/api/users/current`, authHeaders(token));
  },
  async updateCurrentUser(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `/api/users/current`,
      data,
      authHeaders(token)
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`/api/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`/api/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`/api/users`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`/api/recover-password/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`/api/reset-password`, {
      newPassword: password,
      token,
    });
  },
};

const guestsApi = {
  async getCurrentGuest() {
    const path = `/api/guests/current`;
    return client.get<IGuest>(path);
  },
  async getGuest(guestId: string) {
    const path = `/api/guests/${guestId}`;
    return client.get<IGuest>(path);
  },
  async createCurrentGuest(data: IGuestCreate) {
    const path = `/api/guests/current`;
    return client.post(path, data);
  },
  async updateGuest(guestId: string, data: IGuestUpdate) {
    const path = `/api/guests/${guestId}`;
    return client.patch(path, data);
  },
  async deleteGuest(featureId: string, guestId: string) {
    const path = `/api/features/${featureId}/guests/${guestId}`;
    return client.delete(path);
  },
};

const featuresApi = {
  async getFeature(slugOrId: string) {
    const path = `/api/features/${slugOrId}`;
    return client.get<IFeature>(path);
  },
};

export const api = {
  ...accountsApi,
  ...guestsApi,
  ...featuresApi,
};
