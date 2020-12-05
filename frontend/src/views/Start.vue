<template>
  <router-view> </router-view>
</template>

<script lang="ts">
import Vue from "vue";
import { dispatchCheckLoggedIn } from "@/store/main/actions";

export default Vue.extend({
  async created() {
    await dispatchCheckLoggedIn(this.$store);
  },
});
</script>
