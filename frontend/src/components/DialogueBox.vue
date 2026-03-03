<script setup>
import { ref } from 'vue';

const isVisible = ref(false);
const message = ref('');
let resolvePromise;

// Function to open the dialog
const open = (msg) => {
    message.value = msg;
    isVisible.value = true;
    return new Promise((resolve) => {
        resolvePromise = resolve;
    });
};

const handleConfirm = () => {
    isVisible.value = false;
    resolvePromise(true);
};

const handleCancel = () => {
    isVisible.value = false;
    resolvePromise(false);
};

defineExpose({ open });
</script>

<template>
    <div v-if="isVisible"
        class="fixed min-h-screen inset-0 z-100 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
        <div
            class="bg-white rounded-4xl p-8 max-w-sm w-full shadow-2xl border border-slate-100 animate-in fade-in zoom-in duration-200">
            <div class="text-center">
                <div
                    class="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl">
                    ❓
                </div>
                <h3 class="text-xl font-bold text-slate-900 mb-2">Confirm Action</h3>
                <p class="text-slate-500 mb-8 leading-relaxed">{{ message }}</p>
            </div>

            <div class="flex gap-3">
                <button @click="handleCancel"
                    class="flex-1 px-6 py-3.5 rounded-xl font-bold text-slate-500 bg-slate-100 hover:bg-slate-200 transition active:scale-95">
                    Cancel
                </button>
                <button @click="handleConfirm"
                    class="flex-1 px-6 py-3.5 rounded-xl font-bold text-white bg-[#2563eb] hover:bg-blue-700 shadow-lg shadow-blue-500/20 transition active:scale-95">
                    Yes, proceed
                </button>
            </div>
        </div>
    </div>
</template>
