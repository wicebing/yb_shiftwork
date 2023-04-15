<script setup>
import { NTimeline, NTimelineItem } from 'naive-ui'

</script>

<template>
    <div class="p-2 flex items-center justify-between bg-gray-100 rounded-xl">
        <div>
            <NuxtLink to="/shifts/1">
                <h3 class="py-2 text-xl font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">Shift</h3>
            </NuxtLink>
            <p class="text-gray-600 text-center">posted 2023/04/01</p>
        </div>
        <div style="overflow: auto">
            <n-timeline horizontal>
            <n-timeline-item
                title="pre Staff Name"
                content="Success content"
                time="2018-04-03 20:46"
            />
            <n-timeline-item
                type="error"
                title="Staff Name"
                content="Warning content"
                time="2018-04-03 20:46"
            />
            <n-timeline-item
                type="warning"
                title="Next Staff Name"
                content="Info content"
                time="2018-04-03 20:46"
            />
            </n-timeline>
        </div>
    </div>
</template>