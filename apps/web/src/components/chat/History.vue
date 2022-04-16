<template>
  <div class="history" ref="history">
    <div class="content">
      <ChatMessage
        v-for="message in messages"
        :key="+message.timestamp"
        :color="message.type === MessageType.REQUEST ? 'red' : 'green'"
        :side="message.type === MessageType.REQUEST ? 'right' : 'left'"
        :timestamp="message.timestamp"
      >
        <component :is="message.getRenderComponent()" :message="message" />
      </ChatMessage>
      <div class="empty" v-if="!messages.length" key="empty">
        <span>No messages in history</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, PropType, ref, watch } from 'vue';
import { Message } from '../../domain/chat/models/message.model';
import ChatMessage from './Message.vue';
import { MessageType } from '../../domain/chat/enums/message-type.enum';
const props = defineProps({
  messages: {
    type: Array as PropType<Message[]>,
    default: () => [],
  },
});
const history = ref<HTMLDivElement | null>(null);
watch(
  () => props.messages.length,
  async () => {
    if (history.value) {
      await nextTick();
      history.value.scroll({
        top: history.value.scrollHeight,
        behavior: 'smooth',
      });
    }
  }
);

onMounted(() => {
  if (history.value) {
    history.value.scrollTop = 999999;
  }
});
</script>

<style scoped lang="scss">
.history {
  flex: 1;
  padding: 16px 16px 16px 16px;
  overflow-y: scroll;

  scrollbar-width: thin;
  scrollbar-color: $color-text-lighter transparent;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    transition: all 0.5s ease-in-out;
    background-color: white;
    border-radius: 20px;
  }

  &:hover {
    &::-webkit-scrollbar-thumb {
      background-color: $color-text-lighter;
    }
  }

  .content {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    min-height: 100%;
  }

  .empty {
    text-align: center;
    span {
      color: white;
      background-color: $color-green;
      border-radius: 999px;
      padding: 8px 16px;
    }
    margin-bottom: 16px;
  }
}
</style>
