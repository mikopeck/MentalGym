<template>
<game-window/>
<library-completion/>
</template>
  
  <script>
import GameWindow from "./GameWindow.vue";
import LibraryCompletion from '../LibraryCompletion.vue';

export default 
  {
  name: "GamePage",
  components: { GameWindow,LibraryCompletion },
};
</script>
  
<style scoped>

</style>