// store/themeStore.js
import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
    state: () => {
        //darkMode: JSON.parse(window.localStorage.getItem('darkMode')) || !(typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
        const storedDarkMode = window.localStorage.getItem('darkMode');

        return {
            darkMode: storedDarkMode !== null ? JSON.parse(storedDarkMode) : false
        };
    },
    actions: {
        toggleDarkMode() {
            this.darkMode = !this.darkMode;
            if (typeof window !== 'undefined') {
                window.localStorage.setItem('darkMode', this.darkMode);
            }
        }
    }
});
