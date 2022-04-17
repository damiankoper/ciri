import { Serializer } from '@vueuse/core';
import { instanceToPlain, plainToInstance } from 'class-transformer';
import { RenderMethod } from '../enums/render-method.enum';
import { Message } from '../models/message.model';
import { DefaultMessage } from '../models/default-message.model';
import { IResponseMessage } from '../interfaces/response-message.interface';
import { MessageType } from '../enums/message-type.enum';
import { ErrorMessage } from '../models/error-message.model';

export class MessageSerializer implements Serializer<Message[]> {
  read(raw: string): Message[] {
    return this.transformPlain(JSON.parse(raw));
  }

  write(value: Message[]): string {
    return JSON.stringify(instanceToPlain(value));
  }

  transformPlain(plain: Record<any, any>[]): Message[] {
    return plain.map((m: Record<any, any>) => {
      switch (m.renderMethod) {
        default:
        case RenderMethod.DEFAULT:
          return plainToInstance(DefaultMessage, m);
        case RenderMethod.ERROR:
          return plainToInstance(ErrorMessage, m);
      }
    });
  }

  mapResponseToPlain(messages: IResponseMessage[]): any[] {
    return messages.map((m) => {
      if (m.text) {
        return {
          type: MessageType.RESPONSE,
          renderMethod: RenderMethod.DEFAULT,
          payload: { message: m.text || '' },
        };
      } else {
        return {
          type: MessageType.RESPONSE,
          renderMethod: m.custom?.type,
          payload: m.custom,
        };
      }
    });
  }
}
