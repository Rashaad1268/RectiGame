<script lang="ts">
    export let value: string | undefined = undefined;
</script>

<textarea {...$$restProps} on:change bind:value />

<style lang="scss">
    textarea {
        @apply flex min-h-[80px] w-full text-sm ring-offset-discordDark-830
        focus-visible:outline-none focus-visible:ring-2
        focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50
        resize-none mb-2 px-2 py-3 border border-gray-500 bg-discordDark-830
      rounded-[4px] ease-out;

        &:focus {
            outline: none;
            box-shadow: none;
        }

        &::placeholder {
            @apply text-gray-400;
        }
    }
</style>
