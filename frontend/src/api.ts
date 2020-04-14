import axios from "axios";
import applyConverters from "axios-case-converter";
import { IGuest, IGuestUpdate, IGuestCreate } from "@/interfaces";
import { IFeature } from "@/interfaces";

const client = applyConverters(axios.create());

const featuresApi = {
  async getFeature(slugOrId: string) {
    const path = `/api/features/${slugOrId}`;
    return client.get<IFeature>(path);
  }
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
  }
};

export default {
  ...guestsApi,
  ...featuresApi
};
