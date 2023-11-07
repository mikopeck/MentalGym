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
            if (this.sideMenuOpen) {
                this.setupClickAwayListenerSideMenu();
            }
        },
        hideSideMenu() {
            this.sideMenuOpen = false;
        },
        openSideMenu() {
            this.sideMenuOpen = true;
            this.setupClickAwayListenerSideMenu();
        },

        toggleActionMenu() {
            this.actionsMenuOpen = !this.actionsMenuOpen;
            if (this.actionsMenuOpen) {
                this.setupClickAwayListenerActionMenu();
            }
        },
        hideActionMenu() {
            this.actionsMenuOpen = false;
        },
        openActionMenu() {
            this.actionsMenuOpen = true;
            this.setupClickAwayListenerActionMenu();
        },

        setupClickAwayListenerActionMenu() {
            setTimeout(() => {
                const clickAwayListener = (event) => {
                    const menuElement = document.querySelector('.action-menu');
                    if (!menuElement.contains(event.target)) {
                        this.hideActionMenu();
                        document.removeEventListener('click', clickAwayListener);
                    }
                };
                document.addEventListener('click', clickAwayListener);
            }, 0);
        },

        setupClickAwayListenerSideMenu() {
            setTimeout(() => {
                const clickAwayListener = (event) => {
                    const sideMenuElement = document.querySelector('.side-menu');
                    if (!sideMenuElement.contains(event.target)) {
                        this.hideSideMenu();
                        document.removeEventListener('click', clickAwayListener);
                    }
                };
                document.addEventListener('click', clickAwayListener);
            }, 0);
        }
    },
});
