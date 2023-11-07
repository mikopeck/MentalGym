// store/themeStore.js
import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
    state: () => ({
        darkMode: !(typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
    }),
    actions: {
        toggleDarkMode() {
            this.darkMode = !this.darkMode;
        }
    }
});
