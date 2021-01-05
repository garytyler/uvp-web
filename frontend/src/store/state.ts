import { MainState } from "./main/state";
import { LiveState } from "./live/state";
import { SocketState } from "./socket/state";

export interface State {
  main: MainState;
  live: LiveState;
  socket: SocketState;
}
