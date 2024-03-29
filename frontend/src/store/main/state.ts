import { IUserProfile, IFeature } from "@/interfaces";

export interface AppNotification {
  content: string;
  type?: "success" | "info" | "warning" | "error";
  showProgress?: boolean | undefined;
}

export interface MainState {
  token: string;
  isLoggedIn: boolean | null;
  logInError: boolean;
  userProfile: IUserProfile | null;
  dashboardMiniDrawer: boolean;
  dashboardShowDrawer: boolean;
  notifications: AppNotification[];
  features: IFeature[];
}
