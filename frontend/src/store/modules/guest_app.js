import axios from "axios";

const state = {
  feature: null
};

const getters = {
  feature: state => state.feature
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/features/${slug}/`)
        .then(response => {
          let feature = response.data;
          commit("SET_FEATURE", feature);
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
