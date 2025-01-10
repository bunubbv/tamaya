<script lang="ts">
  export let size = 'm';

  $: flexSize = {
    xs: 0.1,
    s: 1,
    m: 2,
    l: 3,
    xl: 5
  }[size] || 1;

  $: additionalStyle = size === 'xs' ? 'text-overflow: clip; max-height: 50px;' : '';
</script>


<div style={`flex: ${flexSize}; ${additionalStyle}`}>
  <slot />
</div>


<style>
  div {
    padding: var(--table-pad);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
