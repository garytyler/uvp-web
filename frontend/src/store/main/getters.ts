import { MainState } from "./state";
import { getStoreAccessors } from "typesafe-vuex";
import { State } from "../state";
import { AppNotification } from "@/store/main/state";
import { IUserProfile } from "@/interfaces";

export const getters = {
  hasAdminAccess: (state: MainState): boolean | null => {
    return (
      state.userProfile &&
      state.userProfile.isSuperuser &&
      state.userProfile.isActive
    );
  },
  loginError: (state: MainState): boolean => state.logInError,
  dashboardShowDrawer: (state: MainState): boolean => state.dashboardShowDrawer,
  dashboardMiniDrawer: (state: MainState): boolean => state.dashboardMiniDrawer,
  userProfile: (state: MainState): IUserProfile | null => state.userProfile,
  token: (state: MainState): string => state.token,
  isLoggedIn: (state: MainState): boolean | null => state.isLoggedIn,
  firstNotification: (state: MainState): AppNotification | null =>
    state.notifications.length > 0 ? state.notifications[0] : null,
};

const { read } = getStoreAccessors<MainState, State>("");

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
