<!-- Factoid.vue -->
<template>
  <div v-if="factoidVisible != null && factoidText" class="factoid-overlay" @click="closeFactoid">
  <div class="factoid-box">
    <div class="factoid-content">
      <p>{{ factoidText }}</p>
    </div>
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
    onMounted(() => {
      watch(() => store.factoidVisible, () => {
      }, { immediate: true });
    });
  }
}
</script>

<style scoped>
.factoid-overlay {
  position: absolute;
  height: 100%;
  aspect-ratio: 1 / 1;
  max-width: 100%;
  z-index: 110;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.factoid-box{
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
  z-index: 111;
  font-size: 1.2em;
  background-color: var(--background-haze);
  box-shadow: 0 16px 16px var(--background-color-2t), 0 -16px 16px var(--background-color-2t); 
}
</style>
