<template>
  <div class="logo-large">
    <div class="logo"><i class="mdi mdi-fruit-pear"></i> Ciri</div>
    <div class="ad">
      <ChatMessage
        side="left"
        color="green"
        :timestamp="DateTime.now().minus({ minutes: 5 })"
      >
        A helping hand in you everyday life.
      </ChatMessage>
      <ChatMessage side="right" color="red" :timestamp="DateTime.now()">
        Ask a question and find yourself!
      </ChatMessage>
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatMessage from '../chat/Message.vue';
import { DateTime } from 'luxon';
</script>

<style scoped lang="scss">
.logo-large {
  border-radius: $common-border-radius;
  background-color: $color-orange;
  border: none;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);

  .logo {
    color: white;
    text-align: center;
    margin: 12px;
    i {
      font-size: $logo-large-size;
      margin: 0 -0.25em;
    }

    font-weight: bold;
    font-size: $logo-large-size / 1.25;
  }

  .ad {
    border-radius: $common-border-radius;
    background-color: white;
    padding: 32px 16px 16px 16px;
    max-width: 400px;
  }
}
</style>
