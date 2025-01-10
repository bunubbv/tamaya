<script lang="ts">
  import { convertDateTime, convertFileSize } from "$lib/tools";
  import { _ } from "svelte-i18n";

  export let comment: string = '';
  export let year: number = 0;
  export let trackTotal: number = 0;
  export let durationTotal: number = 0;
  export let fileSizeTotal: number = 0;
</script>


<div class="detail">
  {#if trackTotal === 1}
    {$_('info.track',{values: {track_total: trackTotal}})}, {convertDateTime(durationTotal)} <br>
  {:else}
    {$_('info.tracks',{values: {track_total: trackTotal}})}, {convertDateTime(durationTotal)} <br>
  {/if}

  {year != 0 ? $_('info.year',{values: {year: year}}) : $_('unknown_year')},
  {convertFileSize(fileSizeTotal)} <br>

  {#if comment}
    {comment}
  {/if}
</div>


<style>
  .detail {
    font-size: 85%;
    font-weight: 500;
    color: var(--dark-text-sub);
    text-transform: uppercase;
    padding: var(--space-l) 0;
  }
</style>
