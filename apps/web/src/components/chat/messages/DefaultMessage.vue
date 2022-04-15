<template>
  <div>{{ message.message }}</div>
</template>

<script setup lang="ts">
import { DefaultMessage } from '../../../domain/chat/models/default-message.model';
import { PropType } from 'vue';

const props = defineProps({
  message: {
    type: Object as PropType<DefaultMessage>,
  },
});
</script>
