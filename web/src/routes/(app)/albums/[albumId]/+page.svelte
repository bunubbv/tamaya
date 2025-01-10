<script lang="ts">
  import type { PageData } from './$types';
  import AlbumHeader from '$lib/components/AlbumHeader.svelte';
  import AlbumTable from '$lib/components/AlbumTable.svelte';
  import AlbumFooter from '$lib/components/AlbumFooter.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
</script>


<svelte:head>
  <title>
    {data.album.album
      ? data.album.album : $_('unknown_album')
    } / {data.album.albumartist} • mixel-music
  </title>
</svelte:head>

{#if data.album}
  <AlbumHeader
    album={data.album.album}
    albumId={data.album.album_id}
    albumArtist={data.album.albumartist}
    albumArtistId={data.album.albumartist_id}
    tracks={data.album.tracks.map(track => ({
      ...track,
      album: data.album.album,
      album_id: data.album.album_id}
    ))}
  />
  
  <AlbumTable list={data.album} />

  <AlbumFooter
    comment={data.album.tracks[0].comment}
    durationTotal={data.album.duration_total}
    fileSizeTotal={data.album.filesize_total}
    trackTotal={data.album.tracks.length}
    year={data.album.year != 0 ? data.album.year : 0}
  />
{/if}
