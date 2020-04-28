import { commitSetCurrentFeature } from "@/store/live/mutations";
import { store } from "@/store";
import { IFeature } from "@/interfaces";
import { camelize } from "@ridi/object-case-converter";

export const actions = {
  async receiveCurrentFeature({ commit }, data) {
    const feature: IFeature = data.feature;
    await commitSetCurrentFeature(store, camelize(feature));
  },
};