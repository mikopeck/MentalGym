// stores/menuStore.js
import { defineStore } from 'pinia';

export const useMenuStore = defineStore('menu', {
    state: () => ({
        sideMenuOpen: false,
        actionsMenuOpen: false,
        sideMenuClickListener: null,
        actionMenuClickListener: null,
    }),
    actions: {
// side menu
        toggleSideMenu() {
            this.sideMenuOpen = !this.sideMenuOpen;
            if (this.sideMenuOpen) {
                this.setupClickAwayListenerSideMenu();
            }else {
                this.removeClickAwayListenerSideMenu();
            }
        },
        hideSideMenu() {
            this.removeClickAwayListenerSideMenu();
            this.sideMenuOpen = false;
        },
        openSideMenu() {
            this.sideMenuOpen = true;
            this.setupClickAwayListenerSideMenu();
        },
// action menu
        toggleActionMenu() {
            this.actionsMenuOpen = !this.actionsMenuOpen;
            if (this.actionsMenuOpen) {
                this.setupClickAwayListenerActionMenu();
            }else {
                this.removeClickAwayListenerActionMenu();
            }
        },
        hideActionMenu() {
            this.actionsMenuOpen = false;
            this.removeClickAwayListenerActionMenu();
        },
        openActionMenu() {
            this.actionsMenuOpen = true;
            this.setupClickAwayListenerActionMenu();
        },
// Listeners
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
        },

        removeClickAwayListenerActionMenu() {
            if (this.actionMenuClickListener) {
                document.removeEventListener('click', this.actionMenuClickListener);
                this.actionMenuClickListener = null;
            }
        },

        removeClickAwayListenerSideMenu() {
            if (this.sideMenuClickListener) {
                document.removeEventListener('click', this.sideMenuClickListener);
                this.sideMenuClickListener = null;
            }
        }
    },
});
