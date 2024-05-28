<template>
  <div>
    <MenuBar v-if="checkPath" />
  </div>
  <router-view></router-view>
</template>

<script>
import MenuBar from './components/MenuBar.vue';

export default {
  name: 'App',
  components: {
    MenuBar
  },
  created() {

  },
  computed: {
    checkPath() {
      if (this.$route.path == ('/') || this.$route.path.includes('/volume')) {
        return false;
      } else {
        return true;
      }
    }
  },
}

</script>

<style>
button {
  font-family: 'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'PT Sans', 'Nunito', 'Source Sans Pro', 'Playfair Display', sans-serif;
}

#app {
  font-family: 'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'PT Sans', 'Nunito', 'Source Sans Pro', 'Playfair Display', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.center {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

.local-center {
  margin: 0;
  position: absolute;
  left: 50%;
  -ms-transform: translate(-50%);
  transform: translate(-50%);
}
</style>
