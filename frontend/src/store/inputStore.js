// store/inputStore.js
import { defineStore } from 'pinia';

export const useInputStore = defineStore({
    id: 'input',
    state: () => ({
        isInputFieldVisible: true,
    }),
    actions: {
        toggleVisibility() {
            this.isInputFieldVisible = !this.isInputFieldVisible;
        },
        show() {
            this.isInputFieldVisible = true;
        },
        hide() {
            this.isInputFieldVisible = false;
        },
    },
});
