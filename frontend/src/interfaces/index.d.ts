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
