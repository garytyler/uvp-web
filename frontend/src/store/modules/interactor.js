import axios from "axios";

const state = {
  feature: null,
  displayName: null
};

const getters = {
  feature: state => state.feature,
  featureSlug: state => state.feature.slug,
  featureTitle: state => state.feature.title,
  guestList: state => state.feature.guest_queue,
  displayName: state => state.displayName
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  },
  UPDATE_FEATURE(state, feature) {
    state.feature = { ...state.feature, ...feature };
  },
  SET_DISPLAY_NAME(state, displayName) {
    state.displayName = displayName;
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/features/${slug}/`)
        .then(response => {
          commit("SET_FEATURE", response.data);
          resolve(response);
        })
        .catch(error => {
          console.log(error);
          reject(error);
        });
    });
  },
  loadDisplayName({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/guest/`)
        .then(response => {
          let displayName = response.data.name;
          commit("SET_DISPLAY_NAME", displayName);
          resolve(displayName);
        })
        .catch(error => {
          console.log(error);
          reject(error);
        });
    });
  },
  setDisplayName({ commit }, profile) {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/guest/`, profile)
        .then(response => {
          commit("SET_DISPLAY_NAME", response.data.name);
          resolve(response);
        })
        .catch(error => {
          console.log(error);
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
