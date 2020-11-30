export interface IUserProfile {
  email: string;
  isActive: boolean;
  isSuperuser: boolean;
  name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  name?: string;
  password?: string;
  isActive?: boolean;
  isSuperuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  name?: string;
  password?: string;
  isActive?: boolean;
  isSuperuser?: boolean;
}

export interface IPresenter {
  id: string;
}

export interface IGuest {
  id: string;
  name: string;
  feature_id: string;
}

export interface IGuestUpdate {
  name?: string;
  feature_id?: string;
}

export interface IGuestCreate {
  id: string;
  name: string;
}

export interface IFeature {
  id: string;
  title: string;
  guests: IGuest[];
  presenters: IPresenter[];
}
