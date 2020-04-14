<template>
  <router-view></router-view>
</template>

<script lang="ts">
import Vue from "vue";
// import { store } from "../store";
// import {
//   dispatchGetFeature
//   // dispatchGetCurrentGuest
// } from "../store/live/actions";
// import {
//   // readGuest,
//   // readFeature,
//   // readIsCurrentGuestInteractingGuest
// } from "../store/live/getters";

// const startRouteGuard = async (to, from, next) => {
//   const x = `/live/${to.params.featureSlug}`;
//   if ((to.path as string).startsWith(x)) {
//     await dispatchGetFeature(store, { slugOrId: to.params.featureSlug });
//     // await dispatchGetCurrentGuest(store);

//     // const feature = readFeature(store);
//     // const guest = readGuest(store);

//     // }
//     const targetPath = `/live/${to.params.featureSlug}/${mode}`;
//     next(() => {
//       if (targetPath !== to.path) next(targetPath);
//     });
//   }
// };

export default Vue.extend({
  // beforeRouteEnter(to, from, next) {
  //   startRouteGuard(to, from, next);
  // }
  // beforeRouteUpdate(to, from, next) {
  //   startRouteGuard(to, from, next);
  // }
});
</script>
