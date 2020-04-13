import { LiveState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";

export const getters = {
  feature: (state: LiveState) => state.feature,
  guest: (state: LiveState) => state.guest,
  isFeaturePresenterOnline: (state: LiveState) =>
    state.feature &&
    state.feature.presenters &&
    state.feature.presenters.length,
  isCurrentGuestInteractingGuest: (state: LiveState) =>
    state.guest &&
    state.feature &&
    state.feature.guests &&
    state.feature.guests.length > 0 &&
    state.feature.guests[0].id === state.guest.id
};

const { read } = getStoreAccessors<LiveState, State>("live");

export const readFeature = read(getters.feature);
export const readGuest = read(getters.guest);
export const readIsFeaturePresenterOnline = read(
  getters.isFeaturePresenterOnline
);
export const readIsCurrentGuestInteractingGuest = read(
  getters.isCurrentGuestInteractingGuest
);
