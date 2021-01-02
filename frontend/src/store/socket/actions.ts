import { commitSetCurrentFeature } from "@/store/live/mutations";
import { store } from "@/store";
import { IFeature } from "@/interfaces";
import { camelizeKeys } from "humps";

export const actions = {
  async receiveCurrentFeature({}, data: { feature: IFeature }) {
    const feature: IFeature = data.feature;
    await commitSetCurrentFeature(store, camelizeKeys(feature));
  },
};
