<template>
  <div class="logo-large">
    <div class="logo"><i class="mdi mdi-fruit-pear"></i> Ciri</div>
    <div class="ad">
      <ChatMessage
        side="left"
        color="green"
        :timestamp="DateTime.now().minus({ minutes: 5 })"
      >
        A helping hand in your everyday life.
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
    line-height: 1;
    i {
      font-size: $logo-large-size;
      margin: 0 -0.4em;
      display: inline-block;
      transform: rotate(33deg);
    }

    font-weight: bold;
    font-size: math.div($logo-large-size, 1.5);
  }

  .ad {
    border-radius: $common-border-radius;
    background-color: white;
    padding: 32px 16px 16px 16px;
    max-width: 400px;
  }
}
</style>
