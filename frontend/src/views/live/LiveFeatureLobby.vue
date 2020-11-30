<template>
  <div>
    <live-feature-join-modal />
    <live-feature-guest-list-table />
  </div>
</template>

<script>
import LiveFeatureJoinModal from "@/components/LiveFeatureJoinModal.vue";
import LiveFeatureGuestListTable from "@/components/LiveFeatureGuestListTable.vue";

export default {
  name: "live-feature-session-waiting",
  components: { LiveFeatureJoinModal, LiveFeatureGuestListTable },
};
</script>
