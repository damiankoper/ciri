<template>
  <el-main class="main">
    <LogoLarge />
    <Chat />
  </el-main>
</template>

<script setup lang="ts">
import LogoLarge from '../logo/LogoLarge.vue';
import Chat from '../chat/Chat.vue';
</script>

<style scoped lang="scss">
.main {
  display: flex;
  align-items: flex-start;
  justify-content: space-evenly;
  min-height: calc(100vh - $footer-height); // 100% - footer
  width: 100%;
  gap: 16px;

  @media (max-width: 768px) {
    padding: 0;
    .logo-large {
      gap: 0px;
      display: none;
    }
  }
}
</style>
