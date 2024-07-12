<!-- Factoid.vue -->
<template>
  <div v-if="factoidVisible != null && factoidText" class="factoid-overlay" @click="closeFactoid">
    <div class="factoid-content">
      <p>{{ factoidText }}</p>
    </div>
  </div>
</template>


<script>
import { useGameStore } from '@/store/gameStore';
import { watch, onMounted } from 'vue';

export default {
  name: "FactoidComponent",
  computed: {
    factoidVisible() {
      const store = useGameStore();
      return store.factoidVisible;
    },
    factoidText() {
      const store = useGameStore();
      // Assuming factoids is an array of objects and factoidVisible is the index
      console.log(store.factoids);
      return store.factoids[store.factoidVisible]?.factoid_text || 'No factoid text';
    }
  },
  methods: {
    closeFactoid () {
      const store = useGameStore();
      store.factoidVisible = null;
    }
  },
  setup() {
    const store = useGameStore();
    console.log("loaded factiod")
    onMounted(() => {
      watch(() => store.factoidVisible, (newVal, oldVal) => {
        console.log('factoidVisible changed from', oldVal, 'to', newVal);
      }, { immediate: true });
    });
  }
}
</script>

<style scoped>
.factoid-overlay {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 96%;
}

.factoid-content {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: left;
  padding: 1em;
  z-index: 1001;
  font-size: 1.2em;
  background-color: var(--background-haze);
  box-shadow: 0 16px 16px var(--background-color-2t), 0 -16px 16px var(--background-color-2t); 
}
</style>
