<template>
  <div class="history-container">
    <div class="history" ref="history">
      <div class="content">
        <ChatMessage
          v-for="message in messages"
          :key="+message.timestamp"
          :color="getColor(message.type)"
          :side="getSide(message.type)"
          :timestamp="message.timestamp"
        >
          <component :is="message.getRenderComponent()" :message="message" />
        </ChatMessage>
        <div class="empty" v-if="!messages.length" key="empty">
          <span>
            <i class="mdi mdi-message-question-outline" /> No messages in
            history
          </span>
        </div>
      </div>
    </div>
    <transition name="el-fade-in">
      <div
        v-if="showScrollBottom"
        @click="scrollBottom"
        class="scroll-bottom"
        key="scrollBottom"
      >
        <span>
          <i class="mdi mdi-arrow-down" />
          Back to current
        </span>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, PropType, ref, watch } from 'vue';
import { Message } from '../../domain/chat/models/message.model';
import ChatMessage from './Message.vue';
import { MessageType } from '../../domain/chat/enums/message-type.enum';
import { useScroll, watchDebounced } from '@vueuse/core';
const props = defineProps({
  messages: {
    type: Array as PropType<Message[]>,
    default: () => [],
  },
});
const history = ref<HTMLDivElement | null>(null);
const scroll = useScroll(history);
const showScrollBottom = ref(false);

onMounted(() => {
  if (history.value) {
    history.value.scrollTop = 999999;
  }
});

watchDebounced(
  () => scroll.arrivedState.bottom,
  (v) => (showScrollBottom.value = !v),
  { debounce: 1000 }
);
watch(
  () => scroll.arrivedState.bottom,
  (v) => {
    if (v) showScrollBottom.value = false;
  }
);

watch(() => props.messages.length, scrollBottom);
async function scrollBottom() {
  await nextTick();
  history.value?.scroll({
    top: history.value.scrollHeight,
    behavior: 'smooth',
  });
}

function getColor(type: MessageType) {
  switch (type) {
    default:
    case MessageType.ERROR:
    case MessageType.REQUEST:
      return 'red';
    case MessageType.RESPONSE:
      return 'green';
  }
}

function getSide(type: MessageType) {
  switch (type) {
    default:
    case MessageType.REQUEST:
      return 'right';
    case MessageType.RESPONSE:
      return 'left';
    case MessageType.ERROR:
      return 'center';
  }
}
</script>

<style scoped lang="scss">
.history-container {
  flex: 1;
  position: relative;
  overflow-y: hidden;
  .history {
    padding: 16px 16px 16px 16px;
    overflow-y: scroll;
    position: relative;
    scrollbar-width: thin;
    scrollbar-color: $color-text-lighter transparent;
    height: 100%;
    width: 100%;
    box-sizing: border-box;

    .content {
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      min-height: 100%;
    }

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

    .empty {
      text-align: center;
      span {
        color: white;
        background-color: $color-green;
        border-radius: 999px;
        padding: 8px 16px;
      }
      margin-bottom: 32px;
    }

    .error {
      text-align: center;
      span {
        color: white;
        background-color: $color-red;
        border-radius: 999px;
        padding: 8px 16px;
      }
      margin: 16px 0 48px 0;
    }
  }
  .scroll-bottom {
    text-align: center;
    position: absolute;
    bottom: 48px;
    left: 0;
    right: 0;
    span {
      cursor: pointer;
      color: white;
      background-color: $color-orange;
      border-radius: 999px;
      padding: 8px 16px;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    }
  }
}
</style>
