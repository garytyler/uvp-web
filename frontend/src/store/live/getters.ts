import { LiveState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { IFeature, IGuest } from "@/interfaces";

export const getters = {
  currentFeature: (state: LiveState): IFeature | null => state.currentFeature,
  currentGuest: (state: LiveState): IGuest | null => state.currentGuest,
  isFeaturePresenterOnline: (state: LiveState): boolean | null =>
    state.currentFeature &&
    state.currentFeature.presenters &&
    state.currentFeature.presenters.length > 0,
  isCurrentGuestInteractingGuest: (state: LiveState): boolean | null =>
    state.currentGuest &&
    state.currentFeature &&
    state.currentFeature.guests &&
    state.currentFeature.guests.length > 0 &&
    state.currentFeature.guests[0].id === state.currentGuest.id,
};

const { read } = getStoreAccessors<LiveState, State>("live");

export const readFeature = read(getters.currentFeature);
export const readGuest = read(getters.currentGuest);
export const readIsFeaturePresenterOnline = read(
  getters.isFeaturePresenterOnline
);
export const readIsCurrentGuestInteractingGuest = read(
  getters.isCurrentGuestInteractingGuest
);
