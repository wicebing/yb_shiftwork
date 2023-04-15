<script lang='ts' setup>
import { NIcon,  } from 'naive-ui'
import { CalendarSharp } from '@vicons/ionicons5'
</script>

<template>
    <div class="flex items-center space-x-4 font-bold font-mono">
        <NuxtLink to="/" class="text-sky-800 hover:text-white">管理</NuxtLink>
        <NuxtLink to="/" class="text-sky-800 hover:text-white">個人</NuxtLink>
        <NuxtLink to="/today" class="text-sky-800 hover:text-white">
        <n-icon size="20" color="#193F85">
            <calendar-sharp />
        </n-icon>
        </NuxtLink>
    </div>
</template>