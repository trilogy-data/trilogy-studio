<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<style>
:root {
  --main-bg-color: #252525;
  --light-bg-color:  #303030;
  --text: #d3d3d3;
  --text-lighter: #d3d3d3;
  --gutter-h: 5;
}

/* Layout helpers */
.expand {
  flex-grow: 1;
}

.layout-center {
  display: flex;
  justify-content: center;
  align-items: center;
}


.gutter {
    position: relative;
    &.gutter-horizontal,
    &.gutter-vertical {
      display: flex;
      background-color: tranparent;
      z-index: 10;
    }
    &.gutter-horizontal {
      width: 0!important;
      cursor: ew-resize;
      &:after {
        height: 100%;
        width: 8px;
        left: -2px;
      }
    }
    &.gutter-vertical {
      cursor: ns-resize;
      height: 0!important;
      &:after {
        height: 8px;
        width: 100%;
        top: -4px;
      }
    }
    &:after {
      content: "";
      display: block;
      position: absolute;
      z-index: 10;
    }
  }
</style>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
  name: 'App',

  components: {
  },

  data: () => ({

  }),
  computed: {
    routerName() {
      return this.$router.currentRoute;
    },
    showMenuNav() {
      return this.routerName !== 'Menu';
    },
    provider() {
      return this.$store.getters.provider;
    },
    ...mapGetters(['isLoggedIn'])
  },
  methods: {
    ...mapActions(['setLoggedIn',]),
    gotoMenu() {
      this.$router.push({ path: 'studio' })
    },
    checkLogin() {
      // return axios.get('http://localhost:3000/logged_in').then((response) => {
      //   if (response.data) {
      //     this.setLoggedIn({ 'provider': response.data });
      //   }
      // }).catch(() => {
      //   this.setLoggedIn({ 'provider': null });
      // })
    }
  },
  mounted() {
    this.checkLogin()
  },
}
</script>
