<script setup>
import { NSelect } from 'naive-ui'
const useStore = useUserStore()
const resultAUTH = ref({})

const props = defineProps({
    // props
    "resultAUTH": {
      type: Object,
      default: () => ({})
    }
})

const emit = defineEmits(['update:resultAUTH'])

const valueSelect= ref(null)

const options = computed(() => {
    console.log('propsResultAUTH',props.resultAUTH)
    return Object.values(props.resultAUTH).map((user, index) => ({
                        label: user.username,
                        value: user.id
                        }));
});

</script>
<template>
    <n-select v-model:value="valueSelect" :options="options" />
    {{ valueSelect }}
</template>