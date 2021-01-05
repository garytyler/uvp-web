import { commitSetCurrentFeature } from "@/store/live/mutations";
import { store } from "@/store";
import { IFeature } from "@/interfaces";
import { camelizeKeys } from "humps";

export const actions = {
  // eslint-disable-next-line  @typescript-eslint/explicit-module-boundary-types
  async receiveCurrentFeature({}, data: { feature: IFeature }) {
    const feature: IFeature = data.feature;
    commitSetCurrentFeature(store, camelizeKeys(feature));
  },
};
