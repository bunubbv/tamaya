import { getTrackList } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const page = parseInt(url.searchParams.get('page') ?? '1', 10);
  const item = parseInt(url.searchParams.get('item') ?? '50', 10);

  try {
    const data = await getTrackList(fetch, page, item);

    return {
      list: data.list,
      title: 'tracks.title',
      page: page,
      item: item,
    };
  }
  catch (error) {
    console.error(error);
  }
};