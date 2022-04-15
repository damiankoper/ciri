<template>
  <el-container direction="vertical">
    <LayoutMain />
    <LayoutFooter />
  </el-container>
  <img src="@/assets/img/bg.jpg" class="bg" />
</template>

<script lang="ts">
import LayoutFooter from "./components/layout/LayoutFooter.vue";
import LayoutMain from "./components/layout/LayoutMain.vue";

</script>

<style lang="scss">
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
  color: $color-text;
}
</style>

<style scoped lang="scss">
.bg {
  position: fixed;
  top: 0;
  left: 0;
  height: calc(100vh - $footer-height + 16px);
  left: -16px;
  top: -16px;
  filter: blur(5px);
  z-index: -1;
}
</style>
