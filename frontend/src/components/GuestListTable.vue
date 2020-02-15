<template>
  <v-data-table
    no-data-text="Queue is empty."
    item-key="name"
    ref="table"
    mobile-breakpoint="0"
    :headers="headers"
    :items="guests"
    @item-selected="onItemSelected"
    class="elevation-4"
    hide-default-footer
    hide-default-header
  >
    <template v-slot:item.name="{ item }">
      <v-chip
        v-if="guests.indexOf(item) === 0"
        color="green"
        text-color="white"
      >
        <v-avatar left class="green darken-4">
          {{ guests.indexOf(item) }}
        </v-avatar>
        {{ item.name }}
      </v-chip>

      <v-chip v-if="guests.indexOf(item) !== 0">
        <v-avatar left class="green darken-4">
          {{ guests.indexOf(item) }}
        </v-avatar>
        {{ item.name }}
      </v-chip>
    </template>

    <template v-slot:item.handle="{ item }">
      <div v-if="guests.indexOf(item) < 2">
        <v-icon small disabled>
          drag_handle
        </v-icon>
      </div>
      <div v-else>
        <div class="handle">
          <v-icon small>
            drag_handle
          </v-icon>
        </div>
      </div>
    </template>

    <template v-slot:item.delete-action="{ item }">
      <v-icon @click="deleteItem(item)">
        delete
      </v-icon>
    </template>

    <template v-slot:item.edit-action="{ item }">
      <div v-if="featureOwner || displayName === item.name">
        <v-icon class="mr-2" @click="editItem(item)">
          edit
        </v-icon>
      </div>
    </template>
  </v-data-table>
</template>

<script>
import Sortable from "sortablejs";
export default {
  props: {
    featureOwner: {
      required: false,
      type: Boolean,
      default: true // Set to false before deployment
    }
  },

  computed: {
    headers() {
      let result = [
        {
          text: "Name",
          align: "start",
          sortable: false,
          value: "name"
        },
        {
          text: "Edit",
          value: "edit-action",
          align: "end",
          sortable: false
        }
      ];
      if (this.featureOwner === true) {
        return [
          {
            text: "Move",
            value: "handle",
            align: "start",
            sortable: false
          },
          ...result,
          {
            text: "Delete",
            align: "end",
            sortable: false,
            value: "delete-action"
          }
        ];
      } else {
        return result;
      }
    },
    guests() {
      return this.$store.getters["guest_app/feature"].guest_queue;
    },
    displayName() {
      return this.$store.getters["guest_app/displayName"];
    }
  },
  methods: {
    editItem(item) {
      console.log(item);
      this.editedIndex = this.guestItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.guestItems.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.guestItems.splice(index, 1);
    },
    onItemSelected(item) {
      item.isSelected = false;
    }
  },

  mounted() {
    let table = this.$refs.table.$el.querySelector("tbody");
    const _self = this;
    Sortable.create(table, {
      handle: ".handle", // Use handle so user can select text
      onEnd({ newIndex, oldIndex }) {
        try {
          const rowSelected = _self.guestItems.splice(oldIndex, 1)[0]; // Get the selected row and remove it
          _self.guestItems.splice(newIndex, 0, rowSelected); // Move it to the new index
        } catch {
          console.error(
            `Reordering not implemented. - newIndex=${newIndex} oldIndex=${oldIndex}`
          );
        }
      }
    });
  }
};
</script>
<style scoped>
.handle {
  cursor: move !important;
  cursor: -webkit-grabbing !important;
}
</style>
