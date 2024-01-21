<template>
  <div class="page-main-container">
    <h1 class="page-title">Knowledge Net</h1>
    <knowledge-graph/>
  </div>
</template>
  
  <script>
import KnowledgeGraph from "../Graphs/KnowledgeGraph.vue";

export default 
  {
  name: "KnowledgePage",
  components: { KnowledgeGraph },
};
</script>
  
<style scoped>

</style>