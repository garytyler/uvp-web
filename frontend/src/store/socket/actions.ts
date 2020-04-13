import { commitSetFeature } from "@/store/live/mutations";
import { store } from "@/store";
import { IFeature } from "@/interfaces";

export const actions = {
  async receiveFeature({ commit }, data) {
    const feature: IFeature = data.feature;
    await commitSetFeature(store, feature);
  }
};
