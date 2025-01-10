<script lang="ts">
  export let type: string = 'text';
  export let name: string = 'text';
  export let placeholder: string = '';
  export let disabled: boolean = false;
  export let width: string = '100%';
  export let value: string = '';
  export let autocomplete: string | undefined = undefined;
  export let required: boolean = false;
</script>


{#if type === 'password'}
  <input
    {name}
    type="password"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{:else if type === 'email'}
  <input
    {name}
    type="email"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{:else}
  <input
    {name}
    type="text"
    bind:value
    {placeholder}
    {autocomplete}
    style:width={width}
    {disabled}
    {required}
  />
{/if}


<style>
  input {
    display: block;
    padding: 12px;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-m);
    color: var(--dark-text);
    font-family: var(--font-family);
    transition: all 0.2s ease;
    backdrop-filter: blur(32px);
  }
</style>
