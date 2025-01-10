<script lang="ts">
  import type { PageData } from './$types';
  import type { ArtistsResponse } from '$lib/interface';
  import {
    removeLinkParams,
    getPaginatedList,
  } from '$lib/tools';
  import ArtistTable from '$lib/components/ArtistTable.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import Textbox from '$lib/components/elements/Textbox.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let artists: ArtistsResponse = data.artists;
  let startNumber: number = data.start;
  let endNumber: number = data.end

  async function changePage(direction: 'next' | 'prev') {
    const { newStart, newEnd, response } = await getPaginatedList(
      fetch,
      direction,
      'artist',
      data.artists.total,
      startNumber,
      39,
    );

    startNumber = newStart;
    endNumber = newEnd;

    if (response) {
      artists = {
        artists: [...response.response.artists],
        total: response.response.total,
      };
    }

    removeLinkParams(
      { start: startNumber.toString(), end: (endNumber).toString() }
    );
  }
</script>


<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

<div>
  <Textbox
    name="search"
    type="search"
    width="316px"
    placeholder={$_('navbar.search')}
  />
</div>

{#if data.artists}
  <ArtistTable artists={artists.artists} />

  <div class='bottom-ctl'>
    <Button
      button='round'
      preload='hover'
      iconName='iconoir:nav-arrow-left'
      on:click={() => changePage('prev')}
    />
    
    <Button
      button='round'
      preload='hover'
      iconName='iconoir:nav-arrow-right'
      disabled={data.end + (data.end - data.start) >= data.artists.total}
      on:click={() => changePage('next')}
    />
  </div>
{/if}


<style>
  .bottom-ctl {
    gap: 12px;
    display: flex;
    justify-content: flex-end;
    margin: var(--space-m) 0;
  }

  div {
    margin-bottom: var(--space-m);
  }
</style>