<script lang="ts">
  import GridItem from "./GridItem.svelte";
  export let items = [];
  let gridContainer;
  let itemsPerPage;

  $: displayedItems = items.slice(0, itemsPerPage);
  $: emptySlots = items.length < 8 ? 8 - items.length : 0;
</script>


<div bind:this={gridContainer}>
  {#each displayedItems as item}
    <slot name="GridItem" {item}></slot>
  {/each}

  {#if emptySlots > 0}
    {#each Array(emptySlots) as _}
      <GridItem />
    {/each}
  {/if}
</div>


<style>
  div {
    display: grid;
    grid-template-columns: repeat(8, minmax(180px, 1fr));
    grid-gap: var(--space-m);
    overflow-x: hidden;
  }

  @media screen and (max-width: 1960px) {
    div {
      grid-template-columns: repeat(6, minmax(180px, 1fr));
    }
  }

  @media screen and (max-width: 1560px) {
    div {
      grid-template-columns: repeat(5, minmax(180px, 1fr));
    }
  }

  @media screen and (max-width: 1360px) {
    div {
      grid-template-columns: repeat(4, minmax(160px, 1fr));
    }
  }

  @media screen and (max-width: 1160px) {
    div {
      grid-template-columns: repeat(3, minmax(160px, 1fr));
    }
  }

  @media screen and (max-width: 860px) {
    div {
      grid-template-columns: repeat(2, minmax(160px, 1fr));
    }
  }
</style>
