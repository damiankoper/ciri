import { Component, ComputedOptions, MethodOptions } from 'vue';
import { Message } from './message.model';
import ArticlesMessageVue from '../../../components/chat/messages/ArticlesMessage.vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';

export interface IArticlesPayload {
  articles: {
    url: string;
    title: string;
  }[];
  location: string;
}

export class ArticlesMessage extends Message {
  payload: IArticlesPayload = {
    articles: [],
    location: '',
  };

  type: MessageType = MessageType.RESPONSE;
  renderMethod: RenderMethod = RenderMethod.ARTICLES;

  constructor() {
    super();
  }

  getRenderComponent(): Component {
    return ArticlesMessageVue;
  }

  getSpeech(): string {
    return `Here are your latest news from ${this.payload.location}`;
  }
}
