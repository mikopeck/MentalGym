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
  width: 100%;
  height: 100%;
  aspect-ratio: 1 / 1;
  max-width: 80vmin;
  max-height: 80vmin;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
  z-index: 1000;
}

.factoid-content {
  text-align: center;
  max-width: 90%;
  padding: 20px;
  border-radius: 8px;
  background-color: var(--background-color-1t);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 1001;
  font-size: 1.2em;
}
</style>
