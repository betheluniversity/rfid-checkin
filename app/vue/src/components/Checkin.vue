<template>
  <tr>
    <td>{{ checkin.id }}</td>
    <td>{{ checkin.completed }}</td>
    <td>{{ checkin.card_id }}</td>
    <td>{{ checkin.scan_datetime }}</td>
    <td>
      <button class="btn btn-secondary" v-on:click="completeCheckin(checkin)">
        complete
      </button>
    </td>
  </tr>
</template>

<script type="text/javascript">
export default {
  props: ["test", "checkin"],
  data() {
    return {
      scan_datetime: "",
    };
  },
  methods: {
    completeCheckin(checkin) {
      const completed = !checkin.complete;
      const id = checkin.id;
      this.$store.dispatch("checkins/updateCheckin", {
        id,
        completed,
      });
    },
  },

  created() {
    // this.scan_datetime = this.checkin.scan_datetime;
    // this.description = this.todo.Description;
    // this.url = this.todo.Url;
    // this.id = this.todo.Id;
    // this.active = this.todo.Active;
  },
};
</script>
