// stores/menuStore.js
import { defineStore } from 'pinia';

export const useMenuStore = defineStore('menu', {
    state: () => ({
        sideMenuOpen: false,
        actionsMenuOpen: false,
    }),
    actions: {
        toggleSideMenu() {
            this.sideMenuOpen = !this.sideMenuOpen;
            this.manageClickAwayListener('side');
        },
        hideSideMenu() {
            this.sideMenuOpen = false;
            this.removeClickAwayListener();
        },
        openSideMenu() {
            this.sideMenuOpen = true;
            this.manageClickAwayListener('side');
        },

        toggleActionMenu() {
            this.actionsMenuOpen = !this.actionsMenuOpen;
            this.manageClickAwayListener('action');
        },
        hideActionMenu() {
            this.actionsMenuOpen = false;
            this.removeClickAwayListener();
        },
        openActionMenu() {
            this.actionsMenuOpen = true;
            this.manageClickAwayListener('action');
        },

        manageClickAwayListener(menuType) {
            const clickAwayListener = (event) => {
                const menuElement = document.querySelector(menuType === 'side' ? '.side-menu' : '.action-menu');
                if (!menuElement.contains(event.target)) {
                    this[menuType === 'side' ? 'hideSideMenu' : 'hideActionMenu']();
                    this.removeClickAwayListener();
                }
            };

            if (this[menuType === 'side' ? 'sideMenuOpen' : 'actionsMenuOpen']) {
                setTimeout(() => {
                    document.addEventListener('click', clickAwayListener);
                }, 0);
            } else {
                this.removeClickAwayListener();
            }
        },

        removeClickAwayListener() {
            document.removeEventListener('click', this.manageClickAwayListener);
        }
    },
});
