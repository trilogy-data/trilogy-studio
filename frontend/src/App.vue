<template>
  <v-app class="app-wrapper">
    <router-view />
  </v-app>
</template>

<style>


/* Layout helpers */
.expand {
  flex-grow: 1;
}

.layout-center {
  display: flex;
  justify-content: center;
  align-items: center;
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
