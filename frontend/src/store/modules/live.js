import axios from "axios";
import applyConverters from "axios-case-converter";

const client = applyConverters(axios.create());

const state = {
  feature: null,
  currentGuest: null
};

const getters = {
  feature(state) {
    return state.feature;
  },
  featureId(state) {
    // return getters.feature?.id;
    return state.feature.id;
  },
  featureTitle(state, getters) {
    return getters.feature ? getters.feature.title : null;
  },
  featureGuests(state, getters) {
    return getters.feature ? getters.feature.guests : [];
  },
  featurePresenterChannel(state, getters) {
    return getters.feature ? getters.feature.presenter_channel : null;
  },
  featurePresenters(state, getters) {
    return getters.feature ? getters.feature.presenters : null;
  },
  isFeaturePresenterOnline(state, getters) {
    return Boolean(getters.featurePresenters?.length > 0);
  },
  currentGuest(state) {
    return state.currentGuest;
  },
  currentGuestId(state, getters) {
    return getters.currentGuest?.id;
  },
  currentGuestName(state, getters) {
    return getters.currentGuest?.name;
  },
  interactingGuest(state) {
    return state.featureGuests?.length ? state.feature.guests[0] : null;
  },
  interactingGuestId(state) {
    return state.featureGuests?.length ? state.feature.guests[0].id : null;
  },
  currentGuestIsInteractingGuest(state, getters) {
    const x =
      getters.interactingGuestId &&
      getters.interactingGuestId === getters.currentGuestId;
    console.log(x);
    return x;
  }
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  },
  UPDATE_FEATURE(state, feature) {
    state.feature = { ...state.feature, ...feature };
  },
  SET_CURRENT_GUEST(state, currentGuest) {
    state.currentGuest = currentGuest;
  },
  DELETE_GUEST(state, guestId) {
    state.feature.guests.filter(i => i.id != guestId);
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      client
        .get(`/api/features/${slug}`)
        .then(response => response.data)
        .then(feature => {
          commit("SET_FEATURE", feature);
          resolve(feature);
        })
        .catch(error => reject(error));
    });
  },
  loadCurrentGuest({ commit }) {
    return new Promise((resolve, reject) => {
      client
        .get(`/api/guests/current`)
        .then(response => response.data)
        .then(currentGuest => {
          commit("SET_CURRENT_GUEST", currentGuest);
          resolve(currentGuest);
        })
        .catch(error => reject(error));
    });
  },
  setCurrentGuest({ commit }, currentGuest) {
    console.log(currentGuest);
    console.log(state.feature.id);
    return new Promise((resolve, reject) => {
      client
        .put(`/api/features/${state.feature.id}/guests/current`, currentGuest)
        .then(response => response.data)
        .then(currentGuest => {
          commit("SET_CURRENT_GUEST", currentGuest);
          resolve(currentGuest);
        })
        .catch(error => reject(error));
    });
  },
  updateGuest({ commit, state }, guest) {
    return new Promise((resolve, reject) => {
      client
        .patch(`/api/feature/${state.feature.slug}/guest/${guest.id}`, guest)
        .then(response => response.data)
        .then(guest => {
          commit("SET_CURRENT_GUEST", guest); //TODO This is wrong. We should have this in an api/guest store module.
          resolve(guest);
        })
        .catch(error => reject(error));
    });
  },
  deleteGuest({ commit, state }, guestId) {
    return new Promise((resolve, reject) => {
      client
        .delete(`/api/features/${state.feature.id}/guests/${guestId}`)
        .then(response => {
          commit("DELETE_GUEST", state.feature, guestId);
          if (response.data === 1) {
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => reject(error));
    });
  },
  // Websocket receivers
  receiveFeature({ commit }, data) {
    console.log(data);
    commit("UPDATE_FEATURE", data.feature);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
