import { Serializer } from '@vueuse/core';
import { instanceToPlain, plainToInstance } from 'class-transformer';
import { RenderMethod } from '../enums/render-method.enum';
import { Message } from '../models/message.model';
import { DefaultMessage } from '../models/default-message.model';

export class MessageSerializer implements Serializer<Message[]> {
  read(raw: string): Message[] {
    return this.transformPlain(JSON.parse(raw) || []);
  }

  transformPlain(plain: Message[]) {
    return plain.map((m: Message) => {
      switch (m.render) {
        default:
        case RenderMethod.DEFAULT:
          return plainToInstance(DefaultMessage, m);
      }
    });
  }

  write(value: Message[]): string {
    return JSON.stringify(instanceToPlain(value));
  }
}
