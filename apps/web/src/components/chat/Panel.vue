<template>
  <div v-loading="loading">
    <hr />
    <div class="panel">
      <textarea
        v-model="message"
        placeholder="Hi! What can you do for me?"
        rows="3"
        ref="textarea"
        @keydown.enter="send"
      />
      <button
        class="button green send"
        :disabled="!message.length"
        @click="send"
        title="send"
      >
        <i class="mdi mdi-send"></i>
      </button>
      <div class="controls">
        <button
          class="button gray del"
          @click="emit('clear')"
          title="Clear message history"
        >
          <i class="mdi mdi-delete"></i>
        </button>

        <button
          class="button gray speaker"
          :disabled="!isSpeechSynthesisSupported"
          @click="
            emit('update:isSpeechSynthesisEnabled', !isSpeechSynthesisEnabled)
          "
          title="Control speech"
        >
          <i
            v-if="!isSpeechSynthesisEnabled || !isSpeechSynthesisSupported"
            class="mdi mdi-volume-off"
          ></i>
          <i v-else class="mdi mdi-volume-high"></i>
        </button>

        <button
          class="button red mic"
          :disabled="!isSpeechRecognitionSupported"
          @click="isSpeechRecognitionEnabled = !isSpeechRecognitionEnabled"
          title="Listen for speech"
        >
          <div
            class="pulse"
            :class="{ 'pulse-on': isListening && isSpeechRecognitionSupported }"
          ></div>
          <i
            v-if="isSpeechRecognitionEnabled && isSpeechRecognitionSupported"
            class="mdi mdi-text-to-speech"
          />
          <i v-else class="mdi mdi-microphone" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLocalStorage, useSpeechRecognition } from '@vueuse/core';
import { ref, watch } from 'vue';
const emit = defineEmits([
  'message',
  'clear',
  'update:isSpeechSynthesisEnabled',
]);
const props = defineProps({
  loading: { type: Boolean, default: false },
  isSpeechPlaying: { type: Boolean, default: false },
  isSpeechSynthesisEnabled: { type: Boolean, default: true },
  isSpeechSynthesisSupported: { type: Boolean, default: false },
});

const message = ref('');
const textarea = ref<HTMLTextAreaElement | null>(null);
const {
  isSupported: isSpeechRecognitionSupported,
  isListening,
  isFinal,
  result: recognitionResult,
  start: startRecognition,
  stop: stopRecognition,
} = useSpeechRecognition();
const isSpeechRecognitionEnabled = useLocalStorage(
  'ciri-speech-recognition',
  false
);

watch(
  [isSpeechRecognitionEnabled, () => props.isSpeechPlaying],
  ([enabled, playing]) => {
    if (enabled && !playing) startRecognition();
    else stopRecognition();
  }
);

watch(recognitionResult, (result) => {
  message.value = result;
});

watch(isFinal, (v) => {
  if (v) send();
});

async function send(e?: KeyboardEvent | MouseEvent) {
  if (!e || !e.shiftKey) {
    if (message.value.length) {
      emit('message', message.value);
    }
    if (textarea.value) textarea.value.focus();
    message.value = '';
    recognitionResult.value = '';
    e?.preventDefault();
  }
}
</script>

<style scoped lang="scss">
@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba($color-red, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 12px rgba($color-red, 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba($color-red, 0);
  }
}

hr {
  margin: 0;
}
.panel {
  display: flex;
  align-items: flex-end;
  position: relative;
  background-color: white;
  box-shadow: 0 0px 14px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);

  textarea {
    resize: none;
    border: none;
    padding: 32px 0 16px 16px;
    outline: none;
    flex: 1;
  }

  .button {
    cursor: pointer;
    transition: all 0.15s ease-in-out;
    line-height: 1;
    border-radius: 999px;
    border: none;
    &:hover:not(:disabled) {
      filter: brightness(112%);
    }
    &:active:not(:disabled) {
      transition: none;
      filter: brightness(88%);
    }
    &.green {
      color: $color-green-darker;
      background-color: $color-green-lighter;
    }
    &.red {
      color: $color-red-darker;
      background-color: $color-red-lighter;
    }
    &:disabled,
    &.gray {
      color: $color-text-darker;
      background-color: $color-text-lighter;
    }
  }
  .send {
    margin: 16px;
    font-size: 20px;
    width: 40px;
    height: 40px;
  }
  .controls {
    display: flex;
    top: 0;
    right: 48px;
    position: absolute;
    z-index: 9999;
    height: 0;
    button {
      transform: translateY(-50%);
      margin-left: 12px;
    }

    .mic {
      width: 48px;
      height: 48px;
      font-size: 28px;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
      .pulse {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 999px;
      }
      .pulse-on {
        display: inline-block;
        animation: pulse 1s infinite;
      }
    }

    .del,
    .speaker {
      width: 32px;
      height: 32px;
      font-size: 16px;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    }
  }
}
</style>
