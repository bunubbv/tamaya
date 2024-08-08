import { getArtistList } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const page = parseInt(url.searchParams.get('page') ?? '1', 10);
  const item = parseInt(url.searchParams.get('item') ?? '40', 10);

  try {
    const data = await getArtistList(page, item);

    return {
      list: data.list,
      page: page,
      item: item,
      total: data.total,
      title: 'Artists',
    };
  }
  catch (error) {
    console.error(error);
  }
};