import axios from "axios";

const state = {
  feature: null,
  sessionGuest: null
};

const getters = {
  feature: state => state.feature,
  sessionGuest: state => state.sessionGuest
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
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/features/${slug}/`)
        .then(response => {
          commit("SET_FEATURE", response.data);
          resolve(response.data);
        })
        .catch(error => {
          console.log(error);
          reject(error);
        });
    });
  },
  loadSessionGuest({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/guest/`)
        .then(response => {
          commit("SET_SESSION_GUEST", response.data);
          resolve(response.data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  setSessionGuest({ commit }, sessionGuest) {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/guest/`, sessionGuest)
        .then(response => {
          commit("SET_SESSION_GUEST", response.data);
          resolve(response.data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  updateGuest({ commit, state }, guest) {
    let guest_id = guest.id;
    let feature_slug = state.feature.slug;
    return new Promise((resolve, reject) => {
      axios
        .patch(`/api/feature/${feature_slug}/guest/${guest_id}/`, guest)
        .then(response => {
          commit("SET_SESSION_GUEST", response.data);
          resolve(response.data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  receiveGuestWebsocketMessage(store, data) {
    store.commit("UPDATE_FEATURE", data.feature);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
