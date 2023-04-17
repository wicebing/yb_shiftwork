<script lang='ts' setup>
import { NLayoutFooter, NLayoutHeader,  } from 'naive-ui'
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