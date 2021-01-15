/* eslint-disable @typescript-eslint/no-use-before-define */
import { api } from "@/api";
import { router } from "@/router";
import {
  getLocalToken,
  removeLocalToken,
  saveLocalToken,
} from "@/services/localStorage.service";
import { AxiosError } from "axios";
import { getStoreAccessors } from "typesafe-vuex";
import { ActionContext } from "vuex";
import { State } from "../state";
import {
  IUserProfileCreate,
  IUserProfileUpdate,
  IFeatureCreate,
  IFeature,
} from "@/interfaces";
import {
  commitAddNotification,
  commitRemoveNotification,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetToken,
  commitSetUserProfile,
  // commitAddUserFeature,
  // setUserFeatures
  commitAddFeature,
  commitRemoveFeature,
  commitRemoveFeaturesByUser,
} from "./mutations";
import { readUserProfile } from "./getters";
import { AppNotification, MainState } from "./state";

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionSignUp(
    context: MainContext,
    payload: IUserProfileCreate
  ): Promise<void> {
    const loadingNotification = { content: "saving", showProgress: true };
    commitAddNotification(context, loadingNotification);
    return api
      .createUser(context.rootState.main.token, payload)
      .then((response) => {
        commitAddNotification(context, {
          type: "success",
          content: `Your account has been created with email address ${response.data.email}. You can now login.`,
        });
      })
      .catch((error) =>
        commitAddNotification(context, {
          type: "error",
          content: error.message,
        })
      )
      .finally(() => commitRemoveNotification(context, loadingNotification));
  },
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string }
  ): Promise<void> {
    return api
      .logInGetToken(payload.username, payload.password)
      .catch(async () => {
        commitSetLogInError(context, true);
        await dispatchLogOut(context);
      })
      .then(async (response) => {
        if (response && response.data.access_token) {
          const token = response.data.access_token;
          saveLocalToken(token);
          commitSetToken(context, token);
          dispatchGetCurrentUserProfile(context)
            .catch(async () => {
              await dispatchLogOut(context);
            })
            .then(async () => {
              commitSetLoggedIn(context, true);
              commitSetLogInError(context, false);
              await dispatchRouteLoggedIn(context);
            });
        } else {
          await dispatchLogOut(context);
        }
      });
  },
  async actionGetCurrentUserProfile(context: MainContext): Promise<void> {
    return api
      .getCurrentUser(context.state.token)
      .catch(async (error) => await dispatchCheckApiError(context, error))
      .then(
        async (response) =>
          response &&
          response.data &&
          commitSetUserProfile(context, response.data)
      );
  },
  async actionUpdateUserProfile(
    context: MainContext,
    payload: IUserProfileUpdate
  ): Promise<void> {
    const loadingNotification = { content: "saving", showProgress: true };
    const genericErrorMsg = "Error updating profile";
    commitAddNotification(context, loadingNotification);
    return api
      .updateCurrentUser(context.state.token, payload)
      .catch(() => {
        commitAddNotification(context, {
          content: genericErrorMsg,
          type: "error",
        });
      })
      .then((response) => {
        if (response) {
          commitSetUserProfile(context, response.data);
          commitAddNotification(context, {
            content: "Profile successfully updated",
            type: "success",
          });
        } else {
          commitAddNotification(context, {
            content: genericErrorMsg,
            type: "error",
          });
        }
      })
      .finally(() => commitRemoveNotification(context, loadingNotification));
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
    commitAddNotification(context, {
      content: "Logged out",
      type: "warning",
    });
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
  async actionRemoveNotification(
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
  async actionSendPasswordResetEmail(
    context: MainContext,
    payload: { email: string }
  ): Promise<void> {
    const loadingNotification = {
      content: "Sending password recovery email",
      showProgress: true,
    };
    commitAddNotification(context, loadingNotification);
    return api
      .sendPasswordResetEmail(payload.email)
      .catch(() =>
        commitAddNotification(context, {
          type: "error",
          content: "Incorrect email or password",
        })
      )
      .then((response) =>
        commitAddNotification(context, {
          type: "success",
          content: response
            ? response.data.msg
            : `Recovery email sent to ${payload.email}`,
        })
      )
      .finally(() => commitRemoveNotification(context, loadingNotification));
  },
  async actionResetPassword(
    context: MainContext,
    payload: { password: string; token: string }
  ): Promise<void> {
    const loadingNotification = {
      content: "Resetting password",
      showProgress: true,
    };
    commitAddNotification(context, loadingNotification);
    return api
      .resetPassword(payload.password, payload.token)
      .then((response) =>
        commitAddNotification(context, {
          type: "success",
          content: response.data.msg,
        })
      )
      .catch(() =>
        commitAddNotification(context, {
          type: "error",
          content: "Error resetting password",
        })
      )
      .finally(() => commitRemoveNotification(context, loadingNotification));
  },
  async actionCreateFeature(
    context: MainContext,
    payload: IFeatureCreate
  ): Promise<IFeature | undefined> {
    const loadingNotification = {
      content: "Creating feature",
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createFeature(context.state.token, payload),
          await new Promise<void>((resolve) =>
            setTimeout(() => resolve(), 500)
          ),
        ])
      )[0];
      commitAddFeature(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        type: "success",
        content: "Feature created",
      });
      return response.data;
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        type: "error",
        content: "Could not create feature",
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetUserFeatures(context: MainContext): Promise<void> {
    const loadingNotification = {
      content: "Loading...",
      showProgress: true,
    };
    commitAddNotification(context, loadingNotification);
    if (!context.state.userProfile) {
      commitRemoveNotification(context, loadingNotification);
      await dispatchLogOut(context);
      return;
    }
    return api
      .getUserFeatures(context.state.token, context.state.userProfile.id)
      .then(async (response) => {
        if (!response.data) {
          // TODO: Log event
        } else {
          if (!context.state.userProfile) {
            await dispatchLogOut(context);
          } else {
            commitRemoveFeaturesByUser(context, context.state.userProfile.id);
            for (const i of response.data) {
              commitAddFeature(context, i);
            }
          }
        }
      })
      .catch(async (error) => {
        if (error.code === 404) {
          if (!context.state.userProfile) {
            await dispatchLogOut(context);
          } else {
            commitRemoveFeaturesByUser(context, context.state.userProfile.id);
          }
        } else {
          // TODO: Log event
        }
      })
      .finally(() => commitRemoveNotification(context, loadingNotification));
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { dispatch } = getStoreAccessors<MainState | any, State>("");

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetCurrentUserProfile = dispatch(
  actions.actionGetCurrentUserProfile
);
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
export const dispatchRemoveNotification = dispatch(
  actions.actionRemoveNotification
);
export const dispatchSendPasswordResetEmail = dispatch(
  actions.actionSendPasswordResetEmail
);
export const dispatchResetPassword = dispatch(actions.actionResetPassword);
export const dispatchCreateFeature = dispatch(actions.actionCreateFeature);
export const dispatchGetUserFeatures = dispatch(actions.actionGetUserFeatures);
