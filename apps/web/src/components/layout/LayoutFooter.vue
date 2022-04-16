<template>
  <el-footer class="footer" height="32px">
    <span>
      Copyright © {{ new Date().getFullYear() }} |
      <a href="https://github.com/damiankoper" target="_blank">
        @damiankoper
      </a>
      |
      <a href="https://github.com/hergerr" target="_blank"> @hergerr </a>
    </span>
    <span class="love">Made with ❤️</span>
  </el-footer>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.footer {
  text-align: center;
  overflow: hidden;
  padding: 4px 8px;
  font-size: 16px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
  position: relative;

  a {
    text-decoration: none;
    color: inherit;
  }
  @media (max-width: 768px) {
    display: none;
    .love {
      display: none;
    }
  }
}
</style>
