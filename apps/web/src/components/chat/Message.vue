<template>
  <div class="message-container" :class="[side]">
    <div class="avatar" :class="[side, color]">
      <i v-if="side == 'right'" class="mdi mdi-account" />
      <i v-else-if="side == 'left'" class="mdi mdi-robot-love" />
    </div>
    <div class="message" :class="[side, color]">
      <slot />
    </div>
    <div
      class="time"
      :class="[side, color]"
      :title="timestamp.toLocaleString(DateTime.DATETIME_MED_WITH_SECONDS)"
    >
      {{ relativeTimestamp }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { DateTime } from 'luxon';
import { PropType, ref } from 'vue';
import { useIntervalFn } from '@vueuse/core';

const props = defineProps({
  timestamp: {
    type: Object as PropType<DateTime>,
    required: true,
  },
  color: {
    type: String as PropType<'green' | 'red'>,
    default: 'red',
  },
  side: {
    type: String as PropType<'left' | 'right'>,
    default: 'left',
  },
});

const relativeTimestamp = ref(calcRelativeTimestamp());
function calcRelativeTimestamp() {
  return props.timestamp.toRelative() || '';
}

useIntervalFn(() => (relativeTimestamp.value = calcRelativeTimestamp()), 1000, {
  immediate: true,
});
</script>

<style lang="scss" scoped>
.message-container {
  width: 100%;
  display: grid;
  align-items: flex-end;
  gap: 0 8px;
  margin-bottom: 16px;
  &.left {
    grid-template-columns: 0fr 1fr;
  }
  &.right {
    grid-template-columns: 1fr 0fr;
  }

  .avatar {
    border-radius: $common-border-radius;
    width: $message-avatar-size;
    height: $message-avatar-size;
    padding: 8px;
    box-sizing: border-box;

    &.left {
      grid-column: 1;
    }
    &.right {
      grid-column: 2;
    }
    &.green {
      background-color: rgba($color-green, 0.5);
      color: $color-green;
    }
    &.red {
      background-color: rgba($color-red, 0.5);
      color: $color-red;
    }
  }

  .message {
    max-width: 66%;
    padding: $message-border-radius - 4px $message-border-radius;
    border-radius: $message-border-radius;
    color: white;
    &.left {
      grid-column: 2;
    }
    &.right {
      grid-column: 1;
      grid-row: 1;
      justify-self: flex-end;
    }
    &.green {
      background-color: $color-green;
    }
    &.red {
      background-color: $color-red;
    }
  }

  .time {
    margin: 4px $message-border-radius;
    font-size: 0.75em;

    &.left {
      grid-column: 2;
    }
    &.right {
      grid-column: 1;
      text-align: right;
    }
  }
}
</style>
