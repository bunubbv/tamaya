<script lang="ts">
  import type { PlaylistTrack } from "$lib/interface";
  import {
    getAlbumLink,
    getArtistLink,
    convertDateTime,
  } from "$lib/tools";
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import PlayerService from "$lib/stores/stores";
  import TrackDropdown from "./TrackDropdown.svelte";
  import { _ } from 'svelte-i18n';

  export let list: PlaylistTrack[];
</script>


<Table>
  <TableHead>
    <TableHeadItem size='xs'>#</TableHeadItem>
    <TableHeadItem size='xl'>{$_('label.title')}</TableHeadItem>
    <TableHeadItem size='xl'>{$_('label.album')}</TableHeadItem>
    <TableHeadItem size='l'>{$_('label.artist')}</TableHeadItem>
    <TableHeadItem size="s">{$_('label.time')}</TableHeadItem>
    <TableHeadItem size="xs"></TableHeadItem>
  </TableHead>

  {#each list as item, num}
    <TableBody>
      <TableBodyItem size='xs'>
          <span class="text-sub normal">{num + 1}</span>
        </TableBodyItem>
        
        <TableBodyItem size='xl'>
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-missing-attribute -->
          <a on:click={() =>
            PlayerService.addTrack(
              [{
                album: item.album,
                album_id: item.album_id,
                artist: item.artist,
                artist_id: item.artist_id,
                duration: item.duration,
                title: item.title,
                track_id: item.track_id,
              }]
            )
          }
          on:keydown>
            {item.title}
          </a>
        </TableBodyItem>
  
        <TableBodyItem size="xl">
          <a href='{getAlbumLink(item.album_id)}'>
            {item.album ? item.album : $_('unknown_album')}
          </a>
        </TableBodyItem>
  
        <TableBodyItem size='l'>
          <a href='{getArtistLink(item.artist_id)}'>
            {item.artist}
          </a>
        </TableBodyItem>
  
        <TableBodyItem size='s'>
          {convertDateTime(item.duration)}
        </TableBodyItem>
  
        <TableBodyItem size='xs'>
          <TrackDropdown track={item} />
        </TableBodyItem>

    </TableBody>
  {/each}

</Table>
