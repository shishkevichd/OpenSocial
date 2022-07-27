<template>
  <div class="container">
    <navbar-vue />
    <router-view></router-view>
  </div>
</template>

<script>
import NavbarVue from "./components/Navbar.vue";

export default {
  components: {
    NavbarVue
  }
}
</script>

<style lang="scss">
* {
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>