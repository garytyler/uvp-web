import { IFeature, IGuest } from "@/interfaces";

export interface LiveState {
  currentFeature: IFeature | null;
  currentGuest: IGuest | null;
}
