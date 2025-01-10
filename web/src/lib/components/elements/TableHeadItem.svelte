<script lang="ts">
  export let size = 'm';

  $: flexSize = {
    xs: 0.1,
    s: 1,
    m: 2,
    l: 3,
    xl: 5
  }[size] || 1;
</script>


<div style={`flex: ${flexSize};`}>
  <slot />
</div>


<style>
  div {
    font-size: 75%;
    font-weight: bold;
    color: var(--dark-text-sub);
    text-transform: uppercase;
    letter-spacing: 0.3px;
    padding: var(--table-pad);
  }
</style>
