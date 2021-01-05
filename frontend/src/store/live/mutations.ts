import { getStoreAccessors } from "typesafe-vuex";
import { State } from "@/store/state";
import { LiveState } from "./state";
import { IFeature, IGuest } from "@/interfaces";

export const mutations = {
  setCurrentFeature(state: LiveState, payload: IFeature): void {
    state.currentFeature = payload;
  },
  updateCurrentFeature(state: LiveState, payload: IFeature): void {
    state.currentFeature = { ...state.currentFeature, ...payload };
  },
  setCurrentGuest(state: LiveState, payload: IGuest): void {
    state.currentGuest = payload;
  },
  deleteGuest(state: LiveState, id: string): void {
    if (state.currentFeature) {
      state.currentFeature.guests.filter((i) => i.id != id);
    } else {
      console.error("Cannot delete guest becuase live feature is null.");
    }
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { commit } = getStoreAccessors<LiveState | any, State>("live");

export const commitSetCurrentFeature = commit(mutations.setCurrentFeature);
export const commitUpdateCurrentFeature = commit(
  mutations.updateCurrentFeature
);
export const commitSetCurrentGuest = commit(mutations.setCurrentGuest);
export const commitDeleteGuest = commit(mutations.deleteGuest);
