<template>
  <div>
    <div>
      <button
        v-on:click="setVisibility('all')"
        :class="{ selected: getVisibility == 'all' }"
      >
        All
      </button>
      <button
        v-on:click="setVisibility('completed')"
        :class="{ selected: getVisibility == 'completed' }"
      >
        Completed
      </button>
      <button
        v-on:click="setVisibility('not_completed')"
        :class="{ selected: getVisibility == 'not_completed' }"
      >
        Not Completed
      </button>
    </div>
    <table>
      <thead>
        <th>ID</th>
        <th>Completed</th>
        <th>Card ID</th>
        <th>Datetime</th>
      </thead>
      <Checkin
        v-for="checkin in filteredCheckins"
        :checkin="checkin"
        :test="checkin.scan_datetime"
        :key="checkin.id"
      >
      </Checkin>
    </table>
  </div>
</template>

<script>
import Checkin from "./Checkin";
export default {
  name: "CheckinList",
  components: {
    Checkin,
  },
  props: ["checkins", "filters", "visibility"],
  methods: {
    setVisibility(newVisibility) {
      this.$emit("set-visibility", newVisibility);
    },
  },
  computed: {
    filteredCheckins: function () {
      return this.filters[this.visibility](this.checkins);
    },
    getVisibility: function () {
      return this.visibility;
    },
    remaining: function () {
      return this.filters.active(this.checkins).length;
    },
  },
};
</script>

<style scoped></style>
