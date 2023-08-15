<script lang="ts">
    import FormErrorMessages from "./errorMessages.svelte";


    export let errorMessages: string[] = [];

    interface $$Props extends HTMLFormElement {
        errorMessages?: string[];
    }
</script>


<form {...$$restProps} on:submit|preventDefault>
    <slot />

    <FormErrorMessages bind:errorMessages />
</form> 


<style></style>
