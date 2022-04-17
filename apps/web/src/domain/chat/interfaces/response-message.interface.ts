import { RenderMethod } from '../enums/render-method.enum';

export interface IResponseCustom {
  type: RenderMethod;
}

export interface IResponseCustomDefault extends IResponseCustom {
  type: RenderMethod.DEFAULT;
  text: string;
}

export interface IResponseMessage {
  text?: string;
  custom?: IResponseCustomDefault;
}
