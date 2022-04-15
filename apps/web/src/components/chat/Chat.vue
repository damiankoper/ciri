<template>
  <div class="chat">
    <History :messages="messages" />
    <Panel @message="onMessage" @clear="messages = []" :loading="false" />
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
import { useAxios } from '@vueuse/integrations/useAxios';
import { axios } from '../../plugins/axios';
import { DateTime } from 'luxon';

const messageSerializer = new MessageSerializer();

const sender = useLocalStorage('ciri-sender', uuidv4());
const messages = useLocalStorage<Message[]>('ciri-messages', [], {
  serializer: messageSerializer,
});

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
.chat {
  border-radius: $common-border-radius;
  border: none;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  height: 80vh;
  min-width: 400px;
  width: 30vw;
  background-color: white;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
