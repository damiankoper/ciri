import { Component, ComputedOptions, MethodOptions } from 'vue';
import { Message } from './message.model';
import ErrorMessageVue from '../../../components/chat/messages/ErrorMessage.vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';

export interface IErrorPayload {
  message: string;
}

export class ErrorMessage extends Message {
  payload: IErrorPayload = {
    message: '',
  };

  type: MessageType = MessageType.ERROR;
  renderMethod: RenderMethod = RenderMethod.ERROR;

  constructor(msg: string) {
    super();
    this.payload.message = msg;
  }

  getRenderComponent(): Component {
    return ErrorMessageVue;
  }

  getSpeech(): string {
    return this.payload.message;
  }
}
