import { mutations } from "./mutations";
import { SocketState } from "./state";
import { actions } from "./actions";

const defaultState: SocketState = {
  isConnected: false,
  message: "",
  reconnectError: false
};

export const socketModule = {
  namespaced: false,
  state: defaultState,
  mutations,
  actions
};
