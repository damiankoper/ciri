<template>
  <div>
    Here are your latest news from {{ message.payload.location }}:
    <a
      class="article"
      v-for="article in message.payload.articles"
      :href="article.url"
      target="_blank"
    >
      <i class="mdi mdi-newspaper"></i> {{ article.title }}
    </a>
  </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';
import { ArticlesMessage } from 'apps/web/src/domain/chat/models/articles-message.model';

defineProps({
  message: {
    type: Object as PropType<ArticlesMessage>,
    required: true,
  },
});
</script>

<style lang="scss" scoped>
.article {
  margin-top: 8px;
  color: white;

  display: block;

  &:not(:hover) {
    text-decoration: none;
  }
}
</style>
