declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'vue-router' {
  export function useRouter(): any
  export function useRoute(): any
  export interface RouteRecordRaw {
    path: string
    name?: string
    component: any
    children?: RouteRecordRaw[]
    meta?: Record<string, any>
    redirect?: string | { name: string }
  }
  export function createRouter(options: any): any
  export function createWebHistory(base?: string): any
}

declare module 'pinia' {
  export function defineStore(id: string, options: any): any
  export function createPinia(): any
} 