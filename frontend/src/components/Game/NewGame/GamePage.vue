<template>
<div class="game-page">
<game-toolbar/>
<game-window/>
<library-completion/>
</div>
</template>

  <script>
import GameWindow from "./GameWindow.vue";
import LibraryCompletion from './LibraryCompletion.vue';
import GameToolbar from './GameToolbar.vue';

export default 
  {
  name: "GamePage",
  components: { GameWindow,LibraryCompletion, GameToolbar },
};
</script>
  
<style scoped>
.game-page{
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>