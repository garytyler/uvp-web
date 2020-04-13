import { IFeature, IGuest } from "@/interfaces";

export interface LiveState {
  feature: IFeature | null;
  guest: IGuest | null;
}
