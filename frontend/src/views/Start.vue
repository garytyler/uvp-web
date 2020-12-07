<template>
  <router-view> </router-view>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "@/store";
import { dispatchCheckLoggedIn } from "@/store/main/actions";

export default Vue.extend({
  async created() {
    await dispatchCheckLoggedIn(store);
  },
});
</script>
