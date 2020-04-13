import { getStoreAccessors } from "typesafe-vuex";
import { State } from "@/store/state";
import { LiveState } from "./state";
import { IFeature } from "@/interfaces";

export const mutations = {
  setFeature(state: LiveState, payload: IFeature) {
    state.feature = payload;
  },
  updateFeature(state: LiveState, payload: IFeature) {
    state.feature = { ...state.feature, ...payload };
  },
  setGuest(state: LiveState, payload) {
    state.guest = payload;
  },
  deleteGuest(state: LiveState, payload) {
    if (state.feature) {
      state.feature.guests.filter(i => i.id != payload);
    } else {
      console.error("Cannot delete guest becuase live feature is null.");
    }
  }
};

const { commit } = getStoreAccessors<LiveState | any, State>("live");

export const commitSetFeature = commit(mutations.setFeature);
export const commitUpdateFeature = commit(mutations.updateFeature);
export const commitSetGuest = commit(mutations.setGuest);
export const commitDeleteGuest = commit(mutations.deleteGuest);
