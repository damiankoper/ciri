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
      >
        <i class="mdi mdi-send"></i>
      </button>

      <button
        class="button gray del"
        @click="emit('clear')"
        title="Clear message history"
      >
        <i class="mdi mdi-delete"></i>
      </button>

      <button class="button red mic">
        <i v-if="listening" class="mdi mdi-text-to-speach"></i>
        <i class="mdi mdi-microphone"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const emit = defineEmits(['message', 'clear']);
const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
});

const message = ref('');
const textarea = ref<HTMLTextAreaElement | null>(null);
const listening = ref(false);
async function send(e: KeyboardEvent | MouseEvent) {
  if (!e.shiftKey) {
    if (message.value.length) {
      emit('message', message.value);
    }
    if (textarea.value) textarea.value.focus();
    message.value = '';
    e.preventDefault();
  }
}
</script>

<style scoped lang="scss">
hr {
  margin: 0;
}
.panel {
  display: flex;
  align-items: flex-end;
  position: relative;
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
    &:hover {
      filter: brightness(112%);
    }
    &:active {
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

  .mic {
    position: absolute;
    top: -26px;
    right: 48px;
    width: 48px;
    height: 48px;
    font-size: 28px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    z-index: 9999;
  }

  .del {
    position: absolute;
    top: -19px;
    right: 108px;
    width: 32px;
    height: 32px;
    font-size: 16px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    z-index: 9999;
  }
}
</style>
