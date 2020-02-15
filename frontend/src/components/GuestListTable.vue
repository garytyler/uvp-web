<template>
  <b-container>
    <b-card no-body>
      <b-card-text class="mx-2 mt-2 mb-2" id="display-name-label">
        <span class="text-secondary">Queue</span>
      </b-card-text>
      <b-table
        striped
        hover
        caption-top
        small
        no-select-on-click
        thead-class="hidden-table-header"
        :fields="tableFields"
        :items="tableItems"
      >
      </b-table>
    </b-card>
  </b-container>
</template>

<script>
export default {
  name: "GuestApp",
  data() {
    return {
      tableFields: ["index", "name"]
    };
  },
  computed: {
    tableItems() {
      let guests = this.guests;
      const items = [];
      guests.forEach(function(guest, index) {
        items.push({ index: index, name: guests[index].name });
      });
      return items;
    },
    guests() {
      return this.$store.getters["guest_app/feature"].guest_queue;
    }
  }
};
</script>

<style>
.hidden-table-header {
  display: none;
}
</style>
