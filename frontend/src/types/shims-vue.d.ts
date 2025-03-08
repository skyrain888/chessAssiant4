// Vue组件声明
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 声明Vue模块
declare module 'vue' {
  export * from 'vue/dist/vue'
}

// 声明Vue Router模块
declare module 'vue-router' {
  export * from 'vue-router/dist/vue-router'
}

// 声明Pinia模块
declare module 'pinia' {
  export * from 'pinia/dist/pinia'
}

// 声明ArcoDesign模块
declare module '@arco-design/web-vue' {
  export * from '@arco-design/web-vue/es/index'
}

// 声明ArcoDesign图标模块
declare module '@arco-design/web-vue/es/icon' {
  export * from '@arco-design/web-vue/es/icon/index'
}

declare module 'vue' {
  export interface GlobalComponents {
    RouterLink: typeof import('vue-router')['RouterLink']
    RouterView: typeof import('vue-router')['RouterView']
  }
}

// 声明Vue核心API
declare module 'vue' {
  export * from '@vue/runtime-core'
  export * from '@vue/runtime-dom'
}

// 声明Arco Design Vue组件
declare module '@arco-design/web-vue' {
  export const Message: {
    info(content: string, config?: object): void
    success(content: string, config?: object): void
    warning(content: string, config?: object): void
    error(content: string, config?: object): void
  }
  
  export const Notification: {
    info(config: { title?: string; content: string; closable?: boolean }): void
    success(config: { title?: string; content: string; closable?: boolean }): void
    warning(config: { title?: string; content: string; closable?: boolean }): void
    error(config: { title?: string; content: string; closable?: boolean }): void
  }
  
  export const Modal: {
    info(config: { title?: string; content: string; okText?: string; cancelText?: string; onOk?: () => void; onCancel?: () => void }): void
    success(config: { title?: string; content: string; okText?: string; cancelText?: string; onOk?: () => void; onCancel?: () => void }): void
    warning(config: { title?: string; content: string; okText?: string; cancelText?: string; onOk?: () => void; onCancel?: () => void }): void
    error(config: { title?: string; content: string; okText?: string; cancelText?: string; onOk?: () => void; onCancel?: () => void }): void
    confirm(config: { title?: string; content: string; okText?: string; cancelText?: string; onOk?: () => void; onCancel?: () => void }): void
  }
} 