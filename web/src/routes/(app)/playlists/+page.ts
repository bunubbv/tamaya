import { getPlaylists } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const start = parseInt(url.searchParams.get('start') ?? '1', 10);
  const end = parseInt(url.searchParams.get('end') ?? '40', 10);

  try {
    const data = await getPlaylists(fetch, start, end);

    return {
      playlists: data.response,
      title: 'title.playlists',
      start: start,
      end: end,
    };
  }
  catch (error) {
    console.error(error);
  }
};
