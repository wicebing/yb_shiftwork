<script setup>
const props = defineProps({
                id: Number,
                NTUHid: String,
                name: String,
                birthday: String,
                AUTHid: Number
                })
</script>

<template>
    <div class="p-2 flex items-center justify-between bg-gray-100 rounded-xl">
        <div>
            <p class="py-2 font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">{{ props.id }}</p>
        </div>
        <div>
            <p class="py-2 font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">{{ props.NTUHid }}</p>
        </div>
        <div>
            <p class="py-2 font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">{{ props.name }}</p>
        </div>
        <div>
            <p class="py-2 font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">{{ props.birthday }}</p>
        </div>
        <div>
            <p class="py-2 font-bold text-gray-800 hover:bg-white rounded-xl font-semibold text-center">{{ props.AUTHid }}</p>
        </div>
    </div>
</template>