import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    collapsed: false as boolean,
    mobileOpen: false as boolean,
  }),
  actions: {
    toggleSidebar() {
      if (window.innerWidth <= 992) {
        this.mobileOpen = !this.mobileOpen
      } else {
        this.collapsed = !this.collapsed
      }
    },
    closeMobile() {
      this.mobileOpen = false
    },
  },
})
