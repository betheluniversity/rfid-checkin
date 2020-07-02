<template>
  <div>
    <todo-list
      v-on:set-visibility="setVisibility"
      v-bind:todos="todos"
      v-bind:filters="filters"
      v-bind:visibility="visibility"
    ></todo-list>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
