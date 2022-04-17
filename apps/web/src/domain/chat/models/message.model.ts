import { Transform } from 'class-transformer';
import { DateTime } from 'luxon';
import { Component } from 'vue';
import { MessageType } from '../enums/message-type.enum';
import { RenderMethod } from '../enums/render-method.enum';

export abstract class Message {
  @Transform(
    ({ value }) =>
      value instanceof DateTime ? value : DateTime.fromISO(value),
    { toClassOnly: true }
  )
  @Transform(({ value }: { value: DateTime }) => value.toISO(), {
    toPlainOnly: true,
  })
  timestamp: DateTime = DateTime.now();
  type: MessageType = MessageType.REQUEST;
  renderMethod: RenderMethod = RenderMethod.DEFAULT;
  abstract payload: Record<any, any>;

  abstract getRenderComponent(): Component;
  abstract getSpeech(): string;
}
