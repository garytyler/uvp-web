import api from "@/api";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import {
  commitSetFeature,
  commitSetGuest,
  commitDeleteGuest
} from "./mutations";
import { IGuestCreate, IGuestUpdate, IFeature } from "@/interfaces";

import { LiveState } from "./state";

type MainContext = ActionContext<LiveState, State>;

export const actions = {
  async actionGetFeature(context: MainContext, payload: { slugOrId: string }) {
    try {
      // const response = await api.getFeature(payload.slugOrId);
      const response = await api.getFeature(payload.slugOrId);

      if (response.data) {
        commitSetFeature(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionGetCurrentGuest(context: MainContext) {
    try {
      const response = await api.getCurrentGuest();
      if (response.data) {
        commitSetGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionCreateCurrentGuest(context: MainContext, payload: IGuestCreate) {
    if (!context.state.feature) {
      console.error("API ERROR"); // TODO
    } else {
      try {
        const response = await api.createCurrentGuest(payload);
        if (response.data) {
          commitSetGuest(context, response.data);
        }
      } catch (error) {
        console.error(error);
      }
    }
  },
  async actionUpdateGuest(
    context: MainContext,
    payload: { guestId: string; guest: IGuestUpdate }
  ) {
    try {
      const response = await api.updateGuest(payload.guestId, payload.guest);
      if (response.data) {
        commitSetGuest(context, response.data);
      }
    } catch (error) {
      console.error(error);
    }
  },
  async actionDeleteGuest(context: MainContext, payload: { guestId: string }) {
    if (!context.state.feature) {
      console.error("API ERROR"); // TODO
    } else {
      try {
        const response = await api.deleteGuest(
          context.state.feature.id,
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
    await commitSetFeature(context, feature);
  }
};

const { dispatch } = getStoreAccessors<LiveState | any, State>("live");

export const dispatchGetFeature = dispatch(actions.actionGetFeature);
export const dispatchGetCurrentGuest = dispatch(actions.actionGetCurrentGuest);
export const dispatchCreateCurrentGuest = dispatch(
  actions.actionCreateCurrentGuest
);
export const dispatchUpdateGuest = dispatch(actions.actionUpdateGuest);

export const dispatchDeleteGuest = dispatch(actions.actionDeleteGuest);
