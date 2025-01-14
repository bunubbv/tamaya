<script lang="ts">
  import type { PageData } from './$types';
  import PlaylistHeader from '$lib/components/PlaylistHeader.svelte';
  import PlaylistTable from '$lib/components/PlaylistTable.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.item.playlist_title} • mixel-music</title>
</svelte:head>

{#if data.item}
  <PlaylistHeader
    playlist_id={data.item.playlist_id}
    playlist_title={data.item.playlist_title}
    playlist_username={data.item.playlist_username}
    tracks={data.item.tracks}
  />
  
  <PlaylistTable list={data.item.tracks} />

  <!-- <AlbumFooter
    comment={data.album.tracks[0].comment}
    durationTotal={data.album.duration_total}
    fileSizeTotal={data.album.filesize_total}
    trackTotal={data.album.tracks.length}
    year={data.album.year != 0 ? data.album.year : 0}
  /> -->
{/if}
