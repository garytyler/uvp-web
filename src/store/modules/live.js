import axios from "axios";

const state = {
  feature: null,
  sessionGuest: null
};

const getters = {
  feature(state) {
    return state.feature;
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
  isFeaturePresenterOnline(state, getters) {
    return Boolean(getters.featurePresenterChannel?.length > 0);
  },
  sessionGuest(state) {
    return state.sessionGuest;
  },
  sessionGuestId(state, getters) {
    return getters.sessionGuest?.id;
  },
  sessionGuestName(state, getters) {
    return getters.sessionGuest?.name;
  },
  interactingGuest(state) {
    return state.featureGuests?.length ? state.feature.guests[0] : null;
  },
  interactingGuestId(state) {
    return state.featureGuests?.length ? state.feature.guests[0].id : null;
  },
  sessionGuestIsInteractingGuest(state, getters) {
    return (
      getters.interactingGuestId &&
      getters.interactingGuestId === getters.sessionGuestId
    );
  }
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  },
  UPDATE_FEATURE(state, feature) {
    state.feature = { ...state.feature, ...feature };
  },
  SET_SESSION_GUEST(state, sessionGuest) {
    state.sessionGuest = sessionGuest;
  },
  DELETE_GUEST(state, guest_id) {
    state.feature.guests.filter(i => i.id != guest_id);
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/features/${slug}/`)
        .then(response => response.data)
        .then(feature => {
          commit("SET_FEATURE", feature);
          resolve(feature);
        })
        .catch(error => reject(error));
    });
  },
  loadSessionGuest({ commit }, featureSlug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/feature/${featureSlug}/guest/`)
        .then(response => response.data)
        .then(sessionGuest => {
          commit("SET_SESSION_GUEST", sessionGuest);
          resolve(sessionGuest);
        })
        .catch(error => reject(error));
    });
  },
  setSessionGuest({ commit }, sessionGuest) {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/feature/${state.feature.slug}/guest/`, sessionGuest)
        .then(response => response.data)
        .then(sessionGuest => {
          commit("SET_SESSION_GUEST", sessionGuest);
          resolve(sessionGuest);
        })
        .catch(error => reject(error));
    });
  },
  updateGuest({ commit, state }, guest) {
    return new Promise((resolve, reject) => {
      axios
        .patch(`/api/feature/${state.feature.slug}/guest/${guest.id}/`, guest)
        .then(response => response.data)
        .then(guest => {
          commit("SET_SESSION_GUEST", guest); //TODO This is wrong. We should have this in an api/guest store module.
          resolve(guest);
        })
        .catch(error => reject(error));
    });
  },
  deleteGuest({ commit, state }, guestId) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/feature/${state.feature.slug}/guest/${guestId}/`)
        .then(response => response.data)
        .then(data => {
          commit("DELETE_GUEST", state.feature, guestId);
          resolve(data);
        })
        .catch(error => reject(error));
    });
  },
  // Websocket receivers
  receiveFeature({ commit }, data) {
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
