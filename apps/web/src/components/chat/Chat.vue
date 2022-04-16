<template>
  <div
    class="chat-container"
    :class="{ mobile: navigator.userAgentData.mobile }"
  >
    <LogoSmall />
    <div class="chat">
      <History :messages="messages" />
      <Panel @message="onMessage" @clear="messages = []" :loading="false" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Panel from './Panel.vue';
import History from './History.vue';
import { useLocalStorage } from '@vueuse/core';
import { v4 as uuidv4 } from 'uuid';
import { DefaultMessage } from '../../domain/chat/models/default-message.model';
import { MessageType } from '../../domain/chat/enums/message-type.enum';
import { RenderMethod } from '../../domain/chat/enums/render-method.enum';
import { Message } from '../../domain/chat/models/message.model';
import { MessageSerializer } from '../../domain/chat/services/message-serializer.service';
import { axios } from '../../plugins/axios';
import { DateTime } from 'luxon';
import LogoSmall from '../logo/LogoSmall.vue';

const messageSerializer = new MessageSerializer();

const sender = useLocalStorage('ciri-sender', uuidv4());
const messages = useLocalStorage<Message[]>('ciri-messages', [], {
  serializer: messageSerializer,
});
const navigator = window.navigator;
async function onMessage(msg: string) {
  const message = new DefaultMessage(
    sender.value,
    msg,
    MessageType.REQUEST,
    RenderMethod.DEFAULT
  );
  messages.value.push(message);
  const response = await axios.post('webhooks/rest/webhook', {
    sender: sender.value,
    message: msg,
  });
  const now = DateTime.now().toISO();
  response.data.forEach((plain: any) => {
    plain.timestamp = now;
    plain.message = plain.text;
    plain.sender = plain.recipient_id;
  });
  messages.value.push(...messageSerializer.transformPlain(response.data));
}
</script>

<style scoped lang="scss">
.chat-container {
  .chat {
    border-radius: $common-border-radius;
    border: none;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    height: calc(100vh - 3 * $footer-height);
    background-color: white;
    width: 400px;
    overflow: hidden;
    display: flex;
    flex-direction: column;

    @media (max-width: 768px) {
      box-shadow: none;
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
      width: 100%;
      height: 100%;
    }
  }

  @media (max-width: 768px) {
    position: fixed;
    background-color: $color-orange;
    width: 100vw;
    top: 0;
    left: 0;
    display: flex;
    height: 100vh;
    flex-direction: column;
    &.mobile {
      height: calc(100vh - 48px);
    }
  }
}
</style>
