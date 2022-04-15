import { Component, ComputedOptions, MethodOptions } from 'vue';
import { Message } from './message.model';
import DefaultMessageVue from '../../../components/chat/messages/DefaultMessage.vue';

export class DefaultMessage extends Message {
  getRenderComponent(): Component {
    return DefaultMessageVue;
  }
}
