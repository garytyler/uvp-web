import axios from "axios";
import applyConverters from "axios-case-converter";
import { IGuest, IFeature } from "./interfaces";

const client = applyConverters(axios.create());

export const api = {
  async getFeature(slugOrId: string) {
    const path = `/api/features/${slugOrId}`;
    return client.get<IFeature>(path);
  },
  async getCurrentGuest() {
    const path = `/api/guests/current`;
    return client.get(path);
  },
  async putCurrentGuest(featureId: string, data: IGuest) {
    const path = `/api/features/${featureId}/guests/current`;
    return client.put(path, data);
  },
  async updateGuest(featureId: string, guestId: string, data: IGuest) {
    const path = `/api/feature/${featureId}/guest/${guestId}`;
    return client.patch(path, data);
  },
  async deleteGuest(featureId: string, guestId: string) {
    const path = `/api/features/${featureId}/guests/${guestId}`;
    return client.delete(path);
  }
};
