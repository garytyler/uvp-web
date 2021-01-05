import { getStoreAccessors } from "typesafe-vuex";
import { State } from "@/store/state";
import { SocketState } from "./state";
import Vue from "vue";

export const mutations = {
  // Provide low-level state management and logging for websocket activity.
  // https://github.com/nathantsoi/vue-native-websocket#vuex-store-integration
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  SOCKET_ONOPEN(state: SocketState, event) {
    Vue.prototype.$socket = event.currentTarget;
    state.isConnected = true;
  },
  SOCKET_ONCLOSE(state: SocketState): void {
    state.isConnected = false;
  },
  SOCKET_ONERROR(state: SocketState): void {
    console.error(state, event);
  },
  SOCKET_ONMESSAGE(state: SocketState, message: string): void {
    state.message = message;
  },
  SOCKET_RECONNECT(state: SocketState, count: number): void {
    console.info(state, count);
  },
  SOCKET_RECONNECT_ERROR(state: SocketState): void {
    state.reconnectError = true;
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
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
