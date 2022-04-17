<template>
  <div>
    <i class="mdi mdi-alert-circle-outline" />
    {{ message.payload.message }}
  </div>
</template>

<script setup lang="ts">
import { ErrorMessage } from '../../../domain/chat/models/error-message.model';
import { PropType } from 'vue';

const props = defineProps({
  message: {
    type: Object as PropType<ErrorMessage>,
    required: true,
  },
});
</script>
