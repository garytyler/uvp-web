<template>
  <div>
    <guest-join-modal />
    <guest-waiting-list-table />
  </div>
</template>

<script>
import GuestJoinModal from "@/components/GuestJoinModal.vue";
import GuestWaitingListTable from "@/components/GuestWaitingListTable.vue";
import { mapGetters } from "vuex";

export default {
  components: { GuestWaitingListTable, GuestJoinModal },
  methods: {},
  computed: {
    ...mapGetters("interact", ["sessionGuestId", "interactingGuestId"])
  },
  created() {
    this.$store.watch(
      () =>
        this.interactingGuestId !== null &&
        this.interactingGuestId === this.sessionGuestId,
      () => {
        this.$router.push("/feature/interact");
      }
    );
  }
};
</script>
