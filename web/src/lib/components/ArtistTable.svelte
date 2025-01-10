<script lang="ts">
  import type { Artists } from "$lib/interface";
  import { convertDateTime, convertFileSize } from '$lib/tools';
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import { _ } from 'svelte-i18n';

  export let artists: Artists[];
</script>


<Table>
  <TableHead>
    <TableHeadItem size='xl'>{$_('label.artist')}</TableHeadItem>
    <TableHeadItem size='s'>앨범 수</TableHeadItem>
    <TableHeadItem size='s'>트랙 수</TableHeadItem>
    <TableHeadItem size="m">총 용량</TableHeadItem>
    <TableHeadItem size="s">{$_('label.time')}</TableHeadItem>
  </TableHead>

  {#each artists as item}
    <TableBody>
      <TableBodyItem size='xl'>
        <a href='/artists/{item.artist_id}'>
          {item.artist}
        </a>
      </TableBodyItem>

      <TableBodyItem size="s">
        {item.album_total}{$_('label.count')}
      </TableBodyItem>

      <TableBodyItem size='s'>
        {item.track_total}{$_('label.count')}
      </TableBodyItem>

      <TableBodyItem size='m'>
        {convertFileSize(item.filesize_total)}
      </TableBodyItem>

      <TableBodyItem size='s'>
        {convertDateTime(item.duration_total)}
      </TableBodyItem>

    </TableBody>
  {/each}
</Table>
