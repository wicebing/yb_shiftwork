<script lang='ts' setup>
import { NLayoutFooter, NLayoutHeader,  } from 'naive-ui'
// import { useUserStore } from '../composables/user.js'
const useStore = useUserStore()
</script>

<template>
    <div>
        <n-layout-header>
          <nav class="flex items-center justify-between flex-wrap font-mono">
            <NuxtLink to="/" >
                <span class="box-decoration-clone bg-gradient-to-r from-indigo-600 to-pink-500 text-white px-2 font-bold font-mono text-xl">
                  $hift¥₿
                </span>
            </NuxtLink>
            <div v-if=useStore.isAuthenticated>
              <span> Hello, {{ useStore.name }} </span>
              <span class="text-sky-700 font-bold" v-if=useStore.is_staff > ({{ useStore.username }}) </span>
              <span v-if="useStore.username !== useStore.NTUHid" class="text-sky-400"> {{ useStore.NTUHid }}</span>
              <span class="text-pink-600 font-semibold" v-if="!useStore.is_staff" > 等候管理員認證權限中 </span>              
            </div>
            <slot name="header"/>
          </nav>
        </n-layout-header>
        <div>
          <slot name="main"/>
        </div>

        <n-layout-footer class="p-6 flex flex-wrap item-center justify-between font-mono">
            <p class="text-white font-bold ">Copyright (c) 2023 yAbI Lab</p>
            <p class="text-white font-bold">Workforce Shift Management & Scheduling System</p>
            <slot name="footer"/>

        </n-layout-footer>
    </div>
  </template>
  
  <style scoped>
  .n-layout-header {
    background: rgba(0, 104, 189, 0.2);
    padding: 24px;
  }
  .n-layout-footer {
    background: rgba(0, 42, 75, 0.719);
    padding: 24px;
  }

  </style>