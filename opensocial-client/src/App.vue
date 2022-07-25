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