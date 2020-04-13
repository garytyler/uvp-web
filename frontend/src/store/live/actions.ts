import { api } from "@/api";
// import { AxiosError } from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
// import { IGuest } from "@/interfaces";
// import { IFeature } from "@/interfaces";
import {
  commitSetFeature,
  commitSetGuest,
  commitDeleteGuest
} from "./mutations";

import { LiveState } from "./state";

type MainContext = ActionContext<LiveState, State>;

export const actions = {
  async actionGetFeature(context: MainContext, payload: { slugOrId: string }) {
    try {
      const response = await api.getFeature(payload.slugOrId);
      if (response.data) {
        commitSetFeature(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionGetGuest(context: MainContext) {
    try {
      const response = await api.getCurrentGuest();

      if (response.data) {
        commitSetGuest(context, response.data);
      }
    } catch (error) {
      console.log(error);
    }
  },
  async actionUpdateGuest(context: MainContext, payload) {
    console.log(context);
    if (!context.state.feature) {
      console.error("API ERROR"); // TODO
      // return;
      // } else if (context.state.guest) {
      //   console.error("API ERROR"); // TODO
      //   return;
    } else {
      console.error(payload); // TODO
      try {
        const response = await api.putCurrentGuest(
          context.state.feature.id,
          payload
        );
        if (response.data) {
          commitSetGuest(context, response.data);
        }
      } catch (error) {
        console.error(error);
      }
    }
  },
  async actionDeleteGuest(context: MainContext, payload: { guestId: string }) {
    if (!context.state.feature) {
      console.error("API ERROR"); // TODO
    } else {
      // console.log(guestId);
      console.log(payload);
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
  }
};

const { dispatch } = getStoreAccessors<LiveState | any, State>("live");

export const dispatchGetFeature = dispatch(actions.actionGetFeature);
export const dispatchGetGuest = dispatch(actions.actionGetGuest);
export const dispatchUpdateGuest = dispatch(actions.actionUpdateGuest);
export const dispatchDeleteGuest = dispatch(actions.actionDeleteGuest);
