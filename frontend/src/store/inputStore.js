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
            console.log("showing")
            this.isInputFieldVisible = true;
        },
        hide() {
            console.log("hiding")
            this.isInputFieldVisible = false;
        },
    },
});
