import { LiveState } from "./live/state";
import { SocketState } from "./socket/state";

export interface State {
  live: LiveState;
  socket: SocketState;
}
