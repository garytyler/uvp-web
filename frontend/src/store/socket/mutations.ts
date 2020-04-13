import { getStoreAccessors } from "typesafe-vuex";
import { State } from "@/store/state";
import { SocketState } from "./state";
import Vue from "vue";

export const mutations = {
  // Provide low-level state management and logging for websocket activity.
  // https://github.com/nathantsoi/vue-native-websocket#vuex-store-integration
  SOCKET_ONOPEN(state: SocketState, event) {
    Vue.prototype.$socket = event.currentTarget;
    state.isConnected = true;
  },
  SOCKET_ONCLOSE(state: SocketState) {
    state.isConnected = false;
  },
  SOCKET_ONERROR(state: SocketState) {
    console.error(state, event);
  },
  SOCKET_ONMESSAGE(state: SocketState, message) {
    state.message = message;
  },
  SOCKET_RECONNECT(state: SocketState, count) {
    console.info(state, count);
  },
  SOCKET_RECONNECT_ERROR(state: SocketState) {
    state.reconnectError = true;
  }
};

const { commit } = getStoreAccessors<SocketState | any, State>("socket");

/*
 *  Accessors only defined for use in tests
 */
export const commitSocketOnOpen = commit(mutations.SOCKET_ONOPEN);
export const commitSocketOnClose = commit(mutations.SOCKET_ONCLOSE);
export const commitSocketOnError = commit(mutations.SOCKET_ONERROR);
export const commitSocketOnMessage = commit(mutations.SOCKET_ONMESSAGE);
export const commitSocketReconnect = commit(mutations.SOCKET_RECONNECT);
export const commitSocketReconnectError = commit(
  mutations.SOCKET_RECONNECT_ERROR
);
