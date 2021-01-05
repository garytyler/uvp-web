/* eslint-disable @typescript-eslint/no-use-before-define */
import { api } from "@/api";
import { router } from "@/router";
import { getLocalToken, removeLocalToken, saveLocalToken } from "@/utils";
import { AxiosError } from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import { IUserProfileCreate, IUserProfileUpdate } from "@/interfaces";
import {
  commitAddNotification,
  commitRemoveNotification,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetToken,
  commitSetUserProfile,
} from "./mutations";
import { AppNotification, MainState } from "./state";

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionSignUp(
    context: MainContext,
    payload: IUserProfileCreate
  ): Promise<void> {
    const loadingNotification = { content: "saving", showProgress: true };
    commitAddNotification(context, loadingNotification);
    api
      .createUser(context.rootState.main.token, payload)
      .then((resp) => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "success",
          content: `Your account has been created with email address ${resp.data.email}. You can now login.`,
        });
      })
      .catch((err) => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "error",
          content: err.message,
        });
      });
  },
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string }
  ): Promise<void> {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password
      );
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commitSetToken(context, token);
        commitSetLoggedIn(context, true);
        commitSetLogInError(context, false);
        await dispatchGetUserProfile(context);
        await dispatchRouteLoggedIn(context);
        commitAddNotification(context, {
          content: "Logged in",
          type: "success",
        });
      } else {
        await dispatchLogOut(context);
      }
    } catch (err) {
      commitSetLogInError(context, true);
      await dispatchLogOut(context);
    }
  },
  async actionGetUserProfile(context: MainContext): Promise<void> {
    try {
      const response = await api.getCurrentUser(context.state.token);
      if (response.data) {
        commitSetUserProfile(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateUserProfile(
    context: MainContext,
    payload: IUserProfileUpdate
  ): Promise<void> {
    try {
      const loadingNotification = { content: "saving", showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateCurrentUser(context.state.token, payload),
          await new Promise<void>((resolve) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitSetUserProfile(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: "Profile successfully updated",
        type: "success",
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCheckLoggedIn(context: MainContext): Promise<void> {
    if (!context.state.isLoggedIn) {
      let token = context.state.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commitSetToken(context, localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getCurrentUser(token);
          commitSetLoggedIn(context, true);
          commitSetUserProfile(context, response.data);
        } catch (error) {
          await dispatchRemoveLogIn(context);
        }
      } else {
        await dispatchRemoveLogIn(context);
      }
    }
  },
  async actionRemoveLogIn(context: MainContext): Promise<void> {
    removeLocalToken();
    commitSetToken(context, "");
    commitSetLoggedIn(context, false);
  },
  async actionLogOut(context: MainContext): Promise<void> {
    await dispatchRemoveLogIn(context);
    await dispatchRouteLogOut(context);
  },
  async actionUserLogOut(context: MainContext): Promise<void> {
    await dispatchLogOut(context);
    commitAddNotification(context, { content: "Logged out", type: "success" });
  },
  actionRouteLogOut(): void {
    if (router.currentRoute.path !== "/login") {
      router.push("/login");
    }
  },
  async actionCheckApiError(
    context: MainContext,
    payload: AxiosError
  ): Promise<void> {
    if (payload.response) {
      if (payload.response.status === 401) {
        await dispatchLogOut(context);
      }
    }
  },
  actionRouteLoggedIn(): void {
    if (
      router.currentRoute.path === "/login" ||
      router.currentRoute.path === "/"
    ) {
      router.push("/account");
    }
  },
  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number }
  ): Promise<boolean> {
    return new Promise((resolve) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
  async passwordRecovery(
    context: MainContext,
    payload: { username: string }
  ): Promise<void> {
    const loadingNotification = {
      content: "Sending password recovery email",
      showProgress: true,
    };
    commitAddNotification(context, loadingNotification);
    api
      .passwordRecovery(payload.username)
      .then((response) => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "success",
          content: response.data.msg,
        });
      })
      .catch(() => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "error",
          content: "Incorrect username or password",
        });
      });
  },
  async resetPassword(
    context: MainContext,
    payload: { password: string; token: string }
  ): Promise<void> {
    const loadingNotification = {
      content: "Resetting password",
      showProgress: true,
    };
    commitAddNotification(context, loadingNotification);
    api
      .resetPassword(payload.password, payload.token)
      .then((response) => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "success",
          content: response.data.msg,
        });
      })
      .catch(() => {
        commitRemoveNotification(context, loadingNotification);
        commitAddNotification(context, {
          type: "error",
          content: "Error resetting password",
        });
      });
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { dispatch } = getStoreAccessors<MainState | any, State>("");

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchSignUp = dispatch(actions.actionSignUp);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(
  actions.actionUpdateUserProfile
);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
