export interface IGuest {
  id: string;
  name: string;
}

export interface IPresenter {
  id: string;
}

export interface IFeature {
  id: string;
  title: string;
  guests: IGuest[];
  presenters: IPresenter[];
}
