<template>
  <div class="logo-small">
    <div class="logo"><i class="mdi mdi-fruit-pear"></i> Ciri</div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.logo-small {
  @media (min-width: 768px) {
    display: none;
  }
  .logo {
    color: white;
    text-align: center;
    margin: 8px;
    line-height: 1;
    i {
      font-size: $logo-small-size;
      margin: 0 -0.4em;
      display: inline-block;
      transform: rotate(33deg);
    }

    font-weight: bold;
    font-size: $logo-small-size / 1.5;
  }
}
</style>
