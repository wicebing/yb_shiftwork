<script setup>
import { NInput, NButton, NForm, NFormItemRow, NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent, NTransfer, NTabs, NTabPane, NCard, NGrid, NGridItem } from "naive-ui";

const route = useRoute()
const useStore = useUserStore()

const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})

const columns = ref([
    {
      title: '人員',
      key: 'name'
    },
    {
      title: '年齡',
      key: 'age'
    },
    {
      title: '備註',
      key: 'footnote'
    },
])

const columnsRule = ref([
    {
      title: '規則代碼',
      key: 'name'
    },
    {
      title: '描述',
      key: 'description'
    },
    {
      title: 'valueOfRule',
      key: 'valueOfRule',
    },
    {
      title: 'staffOnly',
      key: 'staffOnly',
    },
    {
      title: 'specialGroup',
      key: 'specialGroup',
    },
    {
      title: '使用',
      key: 'switch',
    },
])

const result = reactive ({})
const errors = ref([])
const resultStaff = reactive ({})
const resultRules = reactive ({})
const resultAllRules = reactive ({})
const resultAlldescription = reactive ({})
const resultGroupsCC = reactive ({})
const resultGroupsTT = reactive ({})
const resultGroupsMM = reactive ({})
const resultGroupsICU0 = reactive ({})
const resultGroupsICU1 = reactive ({})
const switchRefs = reactive ({})
const thresholdAge = ref(50)

function calculateAge(birthdayString) {
    const birthday = new Date(birthdayString);
    const today = new Date();

    let years = today.getFullYear() - birthday.getFullYear();
    let months = today.getMonth() - birthday.getMonth();

    // Adjust years and months if the birthday hasn't occurred yet this year
    if (today.getDate() < birthday.getDate()) {
    months--;
    }
    if (months < 0) {
    years--;
    months += 12;
    }
    const age =  years+months/12
    const roundedAge = Math.floor(age * 10) / 10;
    return roundedAge
}

function compareAge(birthdayString) {
    const birthday = new Date(birthdayString);
    const today = new Date();

    let years = today.getFullYear() - birthday.getFullYear();
    let months = today.getMonth() - birthday.getMonth();

    // Adjust years and months if the birthday hasn't occurred yet this year
    if (today.getDate() < birthday.getDate()) {
    months--;
    }
    if (months < 0) {
    years--;
    months += 12;
    }
    const age =  years+months/12
    const boolAge = age > thresholdAge.value
    return boolAge
}

function isStaffInResultGroups(staffToCheck, resultGroups) {
    for (const key in resultGroups) {
    const staff = resultGroups[key];
    if (staff.staff === staffToCheck) {
        return true;
    }
    }
    return false;
}

function isStaffInRuleGroups(resmb) {
    const rulesToShow = reactive ({})
    for (const key in resultRules) {
        const rule = resultRules[key];
        const rule_id = rule.id

        if (switchRefs[key]) {
            const ruleDescription = resultAlldescription[key]
            if (rule.specialGroup) {
                for (const key2 in resultAllRules[key]) {
                    const staff = resultAllRules[key][key2];
                    if (staff.staff === resmb.staff) {
                        rulesToShow[key] = {'description':ruleDescription, 'id':rule_id}
                    }
                }
            } else {
                if (compareAge(resmb.staff_birthday, resultAllRules[key])) {
                    rulesToShow[key] = {'description':`>${resultAllRules[key]}歲,先填假日夜`, 'id':rule_id}
                }
            }
        }
    }
  return rulesToShow
}

async function getProjectAttend () {
    console.log('getProjectAttend')
    for (const key in resultStaff) {
        delete resultStaff[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/projectAttend/?project_id=${props.projectId}&ordering=sequence`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data getProjectAttend',data.value)
            Object.assign(resultStaff, data.value.results)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function getGroup (groupname_name, resulttemp) {
    console.log('getGroup')
    errors.value = []
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/group/?groupname_name=${groupname_name}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data resultGroups',data.value)
            Object.assign(resulttemp, data.value.results)        
        } else {
            console.log('error resultGroups',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error Group',error)
        errors.value.push(error)
    }
}

async function getRules () {
    console.log('getRules')
    errors.value = []
    for (const key in resultRules) {
        delete resultGroups[key];
    }
    try {
        const { data, pending, refresh, error } = await useFetch('/api/rule/?staffOnly=true', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data resultRules',data.value)
            Object.assign(resultRules, data.value.results)  
            for (const key in resultRules) {
                switchRefs[key] = true
            }
            makeRuleActive(resultRules)
        } else {
            console.log('error resultRules',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error Group',error)
        errors.value.push(error)
    }
}

async function makeRuleActive(resultRules) {
    console.log('makeRuleActive')
    for (const key in resultRules) {
        const rule = resultRules[key];
        
        const resulttemp = reactive ({})
        if (switchRefs[key]) {
            resultAlldescription[key]=rule.description
            if (rule.specialGroup) {
                getGroup(rule.valueOfRule, resulttemp)
                resultAllRules[key] = resulttemp
            } else {
                resultAllRules[key] = rule.valueOfRule
                thresholdAge.value = rule.valueOfRule
            }
        } else {
            resultAllRules[key] = resulttemp
            resultAlldescription[key]=null
        }
    }
}

onMounted(() => {
    getProjectAttend()
    getRules()
    
    getGroup('CC', resultGroupsCC)
    getGroup('TT', resultGroupsTT)
    getGroup('MM', resultGroupsMM)
    getGroup('ICU0', resultGroupsICU0)
    getGroup('ICU1', resultGroupsICU1)
})

</script>

<template>
    <n-tabs default-value="rulesGet">    
        <n-tab-pane name="rules" tab="預設額外規則調整">
            <table class="table-auto min-w-full">
                <thead class="bg-gray-50">
                    <tr>
                        <th v-for="col in columnsRule" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                    <tr v-for="(res, rowIndex) in resultRules">
                        <td v-for="col in columnsRule" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                            <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='valueOfRule'">
                                {{ res[col.key] }}
                            </div>
                            <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='valueOfRule'">
                                <n-input v-model:value="res[col.key]" @change="makeRuleActive(resultRules)"/>
                            </div>
                            <n-switch v-if="col.key==='switch'"
                            v-model:value="switchRefs[rowIndex]"
                            @update:value="makeRuleActive(resultRules,rowIndex)" />
                            
                        </td>
                    </tr>
                </tbody>
            </table>
            {{resultAllRules}}
            ----
            {{ resultAlldescription }}

            {{ resultRules }}
        </n-tab-pane>
        <n-tab-pane name="rulesGet" tab="所有人員規則一覽">
            <table class="table-auto min-w-full">
                <thead>
                    <tr>
                        <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(res, rowOuterIndex) in resultStaff" >
                        <tr v-for="(resmb, rowIndex) in res.group_members" class="border border-slate-300">
                            <td v-for="(col, colIndex) in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                <div v-if="col.key==='name'">
                                    {{res.sequence}} - 
                                    <span :class="{'bg-red-200':res.groupname_name==='A', 'bg-red-100':res.groupname_name==='B'}">
                                        {{res.groupname_name}}</span> - 
                                    <span :class="{'bg-green-200':isStaffInResultGroups(resmb.staff,resultGroupsCC),
                                                    'bg-green-400':isStaffInResultGroups(resmb.staff,resultGroupsTT),
                                                    'bg-green-600':isStaffInResultGroups(resmb.staff,resultGroupsMM),
                                                    'bg-green-800':isStaffInResultGroups(resmb.staff,resultGroupsICU0),
                                                    'bg-green-700':isStaffInResultGroups(resmb.staff,resultGroupsICU1),}">
                                    {{ resmb.staff_name }}</span> - 
                                    <span>{{ resmb.staff }}</span>
                                </div>
                                <div v-if="col.key==='age'" 
                                :class="{'bg-yellow-200':compareAge(resmb.staff_birthday, 50)}">
                                    {{ calculateAge(resmb.staff_birthday) }}
                                </div>
                                <div v-if="col.key==='footnote'">
                                    
                                    <template v-for="rule in res.related_rules" >
                                        <li class="bg-blue-100 text-sm">{{rule.description}} {{rule.id}}</li>
                                    </template>
                                    <template v-for="rule in isStaffInRuleGroups(resmb)" >
                                        <li class="bg-red-100 text-sm">{{rule.description}} {{rule.id}}</li>
                                    </template>                       
                                </div>
                            </td>
                        </tr>
                    </template >
                </tbody>
            </table>
        </n-tab-pane>  
    </n-tabs>



</template>

