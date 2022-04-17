<template>
  <div
    class="chat-container"
    :class="{ mobile: navigator?.userAgentData?.mobile }"
  >
    <LogoSmall />
    <div class="chat">
      <History :messages="messages" />
      <Panel
        v-model:is-speech-synthesis-enabled="isSpeechSynthesisEnabled"
        :is-speech-synthesis-supported="isSpeechSynthesisSupported"
        :is-speech-playing="isSpeechPlaying"
        @message="handleRequestMessage"
        @clear="messages = []"
        :loading="isLoadingDebounced"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import Panel from './Panel.vue';
import History from './History.vue';
import LogoSmall from '../logo/LogoSmall.vue';
import { useChat } from '../../domain/chat/composables/useChat';

const navigator = window.navigator;
const {
  messages,
  isLoadingDebounced,
  handleRequestMessage,
  isSpeechPlaying,
  isSpeechSynthesisEnabled,
  isSpeechSynthesisSupported,
} = useChat();
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
