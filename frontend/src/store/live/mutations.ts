import { getStoreAccessors } from "typesafe-vuex";
import { State } from "@/store/state";
import { LiveState } from "./state";
import { IFeature } from "@/interfaces";

export const mutations = {
  setCurrentFeature(state: LiveState, payload: IFeature) {
    state.currentFeature = payload;
  },
  updateCurrentFeature(state: LiveState, payload: IFeature) {
    state.currentFeature = { ...state.currentFeature, ...payload };
  },
  setCurrentGuest(state: LiveState, payload) {
    state.currentGuest = payload;
  },
  deleteGuest(state: LiveState, payload) {
    if (state.currentFeature) {
      state.currentFeature.guests.filter((i) => i.id != payload);
    } else {
      console.error("Cannot delete guest becuase live feature is null.");
    }
  },
};

const { commit } = getStoreAccessors<LiveState | any, State>("live");

export const commitSetCurrentFeature = commit(mutations.setCurrentFeature);
export const commitUpdateCurrentFeature = commit(
  mutations.updateCurrentFeature
);
export const commitSetCurrentGuest = commit(mutations.setCurrentGuest);
export const commitDeleteGuest = commit(mutations.deleteGuest);
