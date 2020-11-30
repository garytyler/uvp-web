<template>
  <router-view></router-view>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "@/store";
import { readHasAdminAccess } from "@/store/main/getters";

const routeGuardAdmin = async (to, from, next) => {
  if (!readHasAdminAccess(store)) {
    next("/account");
  } else {
    next();
  }
};

export default Vue.extend({
  methods: {
    beforeRouteEnter(to, from, next) {
      routeGuardAdmin(to, from, next);
    },
    beforeRouteUpdate(to, from, next) {
      routeGuardAdmin(to, from, next);
    },
  },
});
</script>
