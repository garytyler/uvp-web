import { commitSetFeature } from "@/store/live/mutations";
import { store } from "@/store";
import { IFeature } from "@/interfaces";
import { camelize } from "@ridi/object-case-converter";

export const actions = {
  async receiveFeature({ commit }, data) {
    const feature: IFeature = data.feature;
    await commitSetFeature(store, camelize(feature));
  },
};
