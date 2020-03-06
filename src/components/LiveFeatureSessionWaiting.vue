<template>
  <div>
    <live-feature-join-modal />
    <live-feature-guest-list-table />
  </div>
</template>

<script>
import LiveFeatureJoinModal from "@/components/LiveFeatureJoinModal.vue";
import LiveFeatureGuestListTable from "@/components/LiveFeatureGuestListTable.vue";
import { mapGetters } from "vuex";

export default {
  components: { LiveFeatureJoinModal, LiveFeatureGuestListTable },
  computed: {
    ...mapGetters("live", ["sessionGuestId", "interactingGuestId"])
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.$store.watch(
        (state, getters) => getters["live/sessionGuestIsInteractingGuest"],
        (state, getters) => {
          if (getters["live/sessionGuestIsInteractingGuestGuest"]) {
            vm.$router.push(`/live/${to.params.featureSlug}/interacting`);
          }
        }
      );
    });
  }
};
</script>
