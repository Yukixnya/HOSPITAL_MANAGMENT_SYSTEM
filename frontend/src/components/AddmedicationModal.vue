<script setup>
import { ref } from 'vue';
import { PlusIcon, XIcon, SearchIcon } from 'lucide-vue-next';

defineProps({
    isOpen: Boolean
});

const emit = defineEmits(['close', 'add']);

const formData = ref({
    name: '',
    dosage: '',
    frequency: 'Once daily',
    duration: 30
});

const query = ref('');
const results = ref([]);
let timeout;

const cleanName = (name) => {
    return name
        .replace(/\{.*?\}/g, '')
        .replace(/\(.*?\)/g, '')
        .replace(/Pack.*/i, '')
        .split('/')[0]
        .trim();
};

// API call
const searchMedicines = async (searchQuery) => {
    try {
        const res = await fetch(
            `https://rxnav.nlm.nih.gov/REST/drugs.json?name=${searchQuery}`
        );
        const data = await res.json();

        if (!data?.drugGroup?.conceptGroup) return [];

        const medicines = data.drugGroup.conceptGroup
            .flatMap(g => g.conceptProperties || [])
            .map(item => ({
                name: cleanName(item.name),
                id: item.rxcui
            }))
            .slice(0, 5);
        
            console.log("Search results for query:", searchQuery, medicines);

        return medicines;

    } catch (err) {
        console.error("Search error:", err);
        return [];
    }
};

// Debounced search
const handleSearch = () => {
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
        if (query.value.length < 2) {
            results.value = [];
            return;
        }
        results.value = await searchMedicines(query.value);
    }, 200);
};

const selectMedicine = (med) => {
    formData.value.name = med.name;
    query.value = med.name;
    results.value = [];
};

const handleSubmit = () => {
    emit('add', { ...formData.value });

    formData.value = {
        name: '',
        dosage: '',
        frequency: 'Once daily',
        duration: 30
    };

    query.value = '';
    results.value = [];

    emit('close');
};
</script>
<template>
    <div v-if="isOpen"
        class="fixed inset-0 z-100 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">

        <div
            class="bg-white w-full max-w-lg rounded-2xl shadow-2xl border border-slate-100 animate-in fade-in zoom-in duration-200">

            <div class="px-6 py-4 border-b border-slate-50 flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
                        <PlusIcon class="w-5 h-5" />
                    </div>
                    <h3 class="text-lg font-bold text-slate-800">Add New Medication</h3>
                </div>
                <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600 transition-colors">
                    <XIcon class="w-5 h-5" />
                </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
                <div class="relative">
                    <label class="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 block">
                        Medication Name
                    </label>

                    <div class="relative">
                        <SearchIcon class="absolute left-4 top-3.5 w-4 h-4 text-slate-300" />

                        <input v-model="query" @input="handleSearch" type="text"
                            placeholder="Search medicine (e.g. Aspirin)..."
                            class="w-full pl-11 pr-4 py-3 bg-slate-50 rounded-xl border-transparent focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all text-sm outline-none"
                            required autocomplete="off" />

                        <ul v-if="results.length"
                            class="absolute z-110 mt-2 w-full bg-white border border-slate-200 rounded-xl shadow-xl max-h-56 overflow-y-auto py-2">
                            <li v-for="med in results" :key="med.id" @click="selectMedicine(med)"
                                class="px-4 py-2.5 text-sm hover:bg-blue-50 cursor-pointer flex flex-col border-b border-slate-50 last:border-0">
                                <div class="flex flex-col">

                                    <!-- Generic + Brand -->
                                    <span class="font-bold text-slate-800">
                                        {{ med.name }}
                                        <span v-if="med.brand" class="text-slate-400 font-medium">
                                            ({{ med.brand }})
                                        </span>
                                    </span>

                                    <!-- Optional small tag -->
                                    <span v-if="med.brand" class="text-[10px] text-blue-500 uppercase font-semibold">
                                        Brand
                                    </span>

                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label
                            class="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 block">Dosage</label>
                        <input v-model="formData.dosage" type="text" placeholder="e.g., 5mg"
                            class="w-full px-4 py-3 bg-slate-50 rounded-xl border-transparent focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all text-sm outline-none"
                            required />
                    </div>

                    <div>
                        <label
                            class="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 block">Frequency</label>
                        <select v-model="formData.frequency"
                            class="w-full px-4 py-3 bg-slate-50 rounded-xl border-transparent focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all text-sm outline-none appearance-none">
                            <option value="Once daily">Once daily</option>
                            <option value="Twice daily">Twice daily</option>
                            <option value="Every 8 hours">Every 8 hours</option>
                            <option value="As needed">As needed (PRN)</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label
                        class="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 block">Duration</label>
                    <div class="flex items-center gap-3">
                        <input v-model="formData.duration" type="number"
                            class="w-24 px-4 py-3 bg-slate-50 rounded-xl border-transparent focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all text-sm outline-none" />
                        <span class="text-sm font-bold text-slate-500 uppercase tracking-tight">Days</span>
                    </div>
                </div>

                <div class="pt-4 flex gap-3">
                    <button type="button" @click="$emit('close')"
                        class="flex-1 px-4 py-3 border border-slate-200 text-slate-600 font-bold text-sm rounded-xl hover:bg-slate-50 transition-all">
                        Cancel
                    </button>
                    <button type="submit"
                        class="flex-2 px-4 py-3 bg-blue-600 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all">
                        Add to Prescription
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
