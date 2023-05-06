<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent, NTransfer } from 'naive-ui'
import { NTabs, NTabPane } from 'naive-ui'

const route = useRoute()
const useStore = useUserStore()

const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})

const dateRange = ref()
const paneName = ref('selectDate')
const startDate = ref()
const endDate = ref()
const resultShift = reactive ({})
const optionsSelectShift = ref([]);


const optionsShift = computed(() => {
    console.log('optionsShift', resultShift);

    return Object.values(resultShift).map((Group) => {
        return {
            label: Group.name,
            value: Group.id,
        };
    });
});

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function submitDateRange() { 
    [startDate.value, endDate.value] = dateRange.value.map(date => formatDate(new Date(date)))
    console.log('start',startDate)
    console.log('end',endDate)
    try {
        const { data, pending, refresh, error } = await useFetch('/api/date/', {
            method: 'POST',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
            body: JSON.stringify({
                start_date: startDate.value,
                end_date: endDate.value
            })
        })
        paneName.value = 'selecShift'
    } catch (error) {
        console.error('Error submitting date range:', error)
    }
}

async function submitShiftDate() {
    try {
        const { data, pending, refresh, error } = await useFetch('/api/createProjectSchedules/', {
            method: 'POST',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
            body: JSON.stringify({
                start_date: startDate.value,
                end_date: endDate.value,
                shift_ids: optionsSelectShift.value,
                project: props.projectId
            })
        });

        console.log('Shift dates submitted', data);
    } catch (error) {
        console.error('Error submitting shift dates:', error);
    }
}



async function getShift () {
    console.log('getShift')
    for (const key in resultShift) {
        delete resultShift[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/shift/', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data shift',data.value)
            Object.assign(resultShift, data.value.results)
            console.log('result shift',resultShift)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

onMounted(() => {
    getShift()
})

</script>

<template>
    <div v-if="startDate">
        專案起訖日期：<span class="text-pink-600 font-semibold"> {{ startDate }} </span> ~ 
        <span class="text-pink-600 font-semibold"> {{ endDate }} </span>
    </div>
    
    <n-tabs
    default-value="selectDate"
    v-model:value="paneName">
        <n-tab-pane name="selectDate" tab="Step 1 日期範圍">
            <n-form>
                日期起迄日：
                <n-date-picker
                v-model:value="dateRange"
                update-value-on-close
                panel
                type="daterange"
                :on-confirm="submitDateRange"
                />        
            </n-form>

            班種transfer
            日曆Table
        </n-tab-pane>
        <n-tab-pane name="selecShift" tab="Step 2 班種" v-if="startDate">
            {{ optionsSelectShift }}
            <n-transfer ref="transfer"
                    :options="optionsShift" v-model:value="optionsSelectShift"
                    source-filterable
                    />
            <n-button type="info" @click="submitShiftDate">
                確認班種
            </n-button>
        </n-tab-pane>
    </n-tabs>

</template>