import { api } from "@/api";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import {
  commitSetCurrentFeature,
  commitSetCurrentGuest,
  commitDeleteGuest,
} from "./mutations";
import { IGuestCreate, IGuestUpdate, IFeature } from "@/interfaces";

import { LiveState } from "./state";

type MainContext = ActionContext<LiveState, State>;

export const actions = {
  async actionGetCurrentFeature(
    context: MainContext,
    payload: { slugOrId: string }
  ): Promise<void> {
    try {
      const response = await api.getFeature(payload.slugOrId);

      if (response.data) {
        commitSetCurrentFeature(context, response.data);
      }
    } catch (error) {
      console.debug(error);
    }
  },
  async actionGetCurrentGuest(context: MainContext): Promise<void> {
    try {
      const response = await api.getCurrentGuest();
      if (response.data) {
        commitSetCurrentGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionCreateCurrentGuest(
    context: MainContext,
    payload: IGuestCreate
  ): Promise<void> {
    api
      .createCurrentGuest(payload)
      .then((resp) => {
        if (resp.data) {
          commitSetCurrentGuest(context, resp.data);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
  async actionUpdateCurrentGuest(
    context: MainContext,
    payload: { guestId: string; guest: IGuestUpdate }
  ): Promise<void> {
    try {
      const response = await api.updateGuest(payload.guestId, payload.guest);
      if (response.data) {
        commitSetCurrentGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionDeleteGuest(
    context: MainContext,
    payload: { guestId: string }
  ): Promise<void> {
    if (!context.state.currentFeature) {
      console.log("API ERROR"); // TODO
    } else {
      try {
        const response = await api.deleteGuest(
          context.state.currentFeature.id,
          payload.guestId
        );
        if (response.data) {
          commitDeleteGuest(context, response.data);
        }
      } catch (error) {
        console.log(error);
      }
    }
  },
  async actionReceiveFeature(
    context: MainContext,
    payload: IFeature
  ): Promise<void> {
    const feature: IFeature = payload;
    commitSetCurrentFeature(context, feature);
  },
};

const { dispatch } = getStoreAccessors<LiveState, State>("live");

export const dispatchGetCurrentFeature = dispatch(
  actions.actionGetCurrentFeature
);
export const dispatchGetCurrentGuest = dispatch(actions.actionGetCurrentGuest);
export const dispatchCreateCurrentGuest = dispatch(
  actions.actionCreateCurrentGuest
);
export const dispatchUpdateGuest = dispatch(actions.actionUpdateCurrentGuest);
export const dispatchDeleteGuest = dispatch(actions.actionDeleteGuest);
