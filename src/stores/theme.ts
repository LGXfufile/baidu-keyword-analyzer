import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  const initTheme = () => {
    // 检查localStorage和系统偏好
    const saved = localStorage.getItem('theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
    isDark.value = saved ? saved === 'dark' : prefersDark
    applyTheme()
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }

  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    isDark,
    initTheme,
    toggleTheme,
  }
})