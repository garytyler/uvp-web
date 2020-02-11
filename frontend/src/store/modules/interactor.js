import axios from "axios";

const state = {
  feature: null,
  displayName: null
};

const getters = {
  feature: state => state.feature,
  displayName: state => state.displayName
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  },
  UPDATE_DISPLAY_NAME(state, displayName) {
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
  updateDisplayName({ commit }, displayName) {
    return new Promise((resolve, reject) => {
      axios
        .put(`/api/guest/`, { name: displayName })
        .then(response => {
          commit("UPDATE_DISPLAY_NAME", response.data.name);
          resolve(response);
        })
        .catch(error => {
          console.log(error);
          reject(error);
        });
    });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
