<template>
  <router-view></router-view>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "../store";
import { dispatchGetFeature, dispatchGetGuest } from "../store/live/actions";
import {
  readGuest,
  readIsCurrentGuestInteractingGuest
} from "../store/live/getters";

const startRouteGuard = async (to, from, next) => {
  await dispatchGetFeature(store, { slugOrId: to.params.featureSlug });
  await dispatchGetGuest(store);
  next(vm => {
    const targetPath = `/live/${to.params.featureSlug}/${
      !readGuest(store) || !readIsCurrentGuestInteractingGuest(store)
        ? "waiting"
        : "interacting"
    }`;
    if (targetPath !== to.path) vm.$router.push(targetPath);
  });
};

export default Vue.extend({
  beforeRouteEnter(to, from, next) {
    startRouteGuard(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    startRouteGuard(to, from, next);
  }
});
</script>
