import { MainState } from "./main/state";
import { AdminState } from "./admin/state";
import { LiveState } from "./live/state";
import { SocketState } from "./socket/state";

export interface State {
  main: MainState;
  admin: AdminState;
  live: LiveState;
  socket: SocketState;
}
