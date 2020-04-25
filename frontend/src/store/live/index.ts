import { mutations } from "./mutations";
import { getters } from "./getters";
import { actions } from "./actions";
import { LiveState } from "./state";

const defaultState: LiveState = {
  currentFeature: null,
  currentGuest: null,
};

export const liveModule = {
  namespaced: true,
  state: defaultState,
  mutations,
  actions,
  getters,
};
