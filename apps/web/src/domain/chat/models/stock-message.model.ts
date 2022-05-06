import { Component, ComputedOptions, MethodOptions } from 'vue';
import { Message } from './message.model';
import StockMessageVue from '../../../components/chat/messages/StockMessage.vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';
import { DateTime } from 'luxon';

export interface IStockPayload {
  name: string;
  price: number;
  currency: string;
  ticker: string;
  time: number;
}

export class StockMessage extends Message {
  payload: IStockPayload = {
    name: 'string',
    price: 0,
    currency: '',
    ticker: '',
    time: 0,
  };

  type: MessageType = MessageType.RESPONSE;
  renderMethod: RenderMethod = RenderMethod.STOCK;

  constructor() {
    super();
  }

  getRenderComponent(): Component {
    return StockMessageVue;
  }

  getSpeech(): string {
    return `The price of the ${this.payload.name}
    is ${this.payload.price}
    ${this.payload.currency.toUpperCase()} as of
    ${DateTime.fromSeconds(this.payload.time).toRelativeCalendar()}.`;
  }
}
