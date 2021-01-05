import { MainState } from "./main/state";
import { LiveState } from "./live/state";
import { SocketState } from "./socket/state";
// import { FeaturesState } from "./features/state";

export interface State {
  main: MainState;
  live: LiveState;
  socket: SocketState;
  // features: FeaturesState;
}
