<script lang="ts">
    export let checked: boolean;
</script>

<div class="relative flex ml-auto">
    <input type="checkbox" bind:checked/>
    <span></span>
</div>

<style lang="scss">
    input {
        @apply peer appearance-none cursor-pointer
               border border-gray-300 rounded-full w-12 h-6;

        svg {
            @apply peer-checked:left-7
            transition-all duration-200
            pointer-events-none w-4 h-4
            block absolute top-1 left-1
            rounded-full bg-gray-300;
        }
    }
</style>