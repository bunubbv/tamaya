<script lang="ts">
  import type { PageData } from './$types';
  import type { AlbumsResponse } from '$lib/interface';
  import { getPaginatedList, getAlbumLink, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import GridItemDetail from '$lib/components/elements/GridItemDetail.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let albums: AlbumsResponse = data.albums;
  let startNumber = data.start;
  let loading = false;

  async function loadMoreAlbums() {
    if (loading || (startNumber + 39) >= albums.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'album', albums.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      albums = {
        albums: [...albums.albums, ...response.response.albums],
        total: response.response.total,
      };
    }

    loading = false;
  }
</script>


<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

<InfiniteScroll threshold={100} on:loadMore={loadMoreAlbums}>
  <GridWrap items={albums.albums}>
    <GridItem
      let:item
      slot="GridItem"
      href={getAlbumLink(item.album_id)}
      src={item.album_id}
      alt={item.album ? item.album : $_('unknown_album')}
    >
      <GridItemDetail
        title={item.album ? item.album : $_('unknown_album')}
        titleHref={getAlbumLink(item.album_id)}
        sub={item.albumartist}
        subHref={getArtistLink(item.albumartist_id)}
      />
    </GridItem>
  </GridWrap>
</InfiniteScroll>
