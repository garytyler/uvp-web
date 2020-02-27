import axios from "axios";

const state = {
  feature: null,
  sessionGuest: null
};

const getters = {
  feature(state) {
    return state.feature;
  },
  featureSlug(state) {
    return state.feature ? state.feature.slug : null;
  },
  featureTitle(state) {
    return state.feature ? state.feature.title : null;
  },
  featureGuests(state) {
    return state.feature ? state.feature.guests : null;
  },
  featurePresenterChannel(state) {
    return state.feature ? state.feature.presenter_channel : null;
  },
  sessionGuest(state) {
    return state.sessionGuest;
  },
  sessionGuestId(state) {
    return state.sessionGuest ? state.sessionGuest.id : null;
  },
  sessionGuestName(state) {
    return state.sessionGuest?.name;
  },
  interactingGuest(state) {
    return state.feature?.guests?.length ? state.feature.guests[0] : null;
  },
  interactingGuestId(state) {
    return state.feature?.guests?.length ? state.feature.guests[0].id : null;
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
  deleteGuest({ commit, state }, guest_id) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/feature/${state.feature.slug}/guest/${guest_id}/`)
        .then(response => {
          if (response.status == 204) {
            commit("DELETE_GUEST", state.feature, guest_id);
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // Websocket receivers
  receiveFeature({ commit }, data) {
    commit("SET_FEATURE", data.feature);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
