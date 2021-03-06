import { Component, ComputedOptions, MethodOptions } from 'vue';
import { Message } from './message.model';
import DefaultMessageVue from '../../../components/chat/messages/DefaultMessage.vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';

export interface IDefaultPayload {
  message: string;
}

export class DefaultMessage extends Message {
  payload: IDefaultPayload = {
    message: '',
  };

  type: MessageType = MessageType.REQUEST;
  renderMethod: RenderMethod = RenderMethod.DEFAULT;

  constructor(msg: string) {
    super();
    this.payload.message = msg;
  }

  getRenderComponent(): Component {
    return DefaultMessageVue;
  }

  getSpeech(): string {
    return this.payload.message;
  }
}
