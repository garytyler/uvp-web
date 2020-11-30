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
  ) {
    try {
      const response = await api.getFeature(payload.slugOrId);

      if (response.data) {
        commitSetCurrentFeature(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionGetCurrentGuest(context: MainContext) {
    try {
      const response = await api.getCurrentGuest();
      if (response.data) {
        commitSetCurrentGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionCreateCurrentGuest(context: MainContext, payload: IGuestCreate) {
    if (!context.state.currentFeature) {
      console.error("API ERROR"); // TODO
    } else {
      try {
        const response = await api.createCurrentGuest(payload);
        if (response.data) {
          commitSetCurrentGuest(context, response.data);
        }
      } catch (error) {
        console.log(error);
      }
    }
  },
  async actionUpdateCurrentGuest(
    context: MainContext,
    payload: { guestId: string; guest: IGuestUpdate }
  ) {
    try {
      const response = await api.updateGuest(payload.guestId, payload.guest);
      if (response.data) {
        commitSetCurrentGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionDeleteGuest(context: MainContext, payload: { guestId: string }) {
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
  async actionReceiveFeature(context: MainContext, payload: IFeature) {
    const feature: IFeature = payload;
    await commitSetCurrentFeature(context, feature);
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
