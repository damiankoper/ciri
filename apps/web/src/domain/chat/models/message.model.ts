import { Transform } from 'class-transformer';
import { DateTime } from 'luxon';
import { Component } from 'vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';

export abstract class Message {
  @Transform(({ value }) => DateTime.fromISO(value), { toClassOnly: true })
  @Transform(({ value }: { value: DateTime }) => value.toISO(), {
    toPlainOnly: true,
  })
  timestamp: DateTime;

  type: MessageType;
  render: RenderMethod;

  sender: string;
  message: string;

  constructor(
    sender: string,
    message: string,
    type: MessageType,
    render: RenderMethod
  ) {
    this.timestamp = DateTime.now();
    this.sender = sender;
    this.message = message;
    this.type = type;
    this.render = render;
  }

  abstract getRenderComponent(): Component;
}
