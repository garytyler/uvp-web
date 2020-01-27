<template>
  <div>
    <h2>{{ feature }}</h2>
    <GuestNameEditor />
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import GuestNameEditor from "@/components/GuestNameEditor.vue";

export default {
  name: "GuestApp",
  components: { GuestNameEditor },
  computed: mapState({
    feature: state => state.guest_app.feature
  }),
  methods: mapActions("guest_app", ["loadFeature"])
};
</script>

<style></style>
