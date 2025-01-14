import { getArtists } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const start = parseInt(url.searchParams.get('start') ?? '1', 10);
  const end = parseInt(url.searchParams.get('end') ?? '40', 10);

  try {
    const data = await getArtists(fetch, start, end);

    return {
      artists: data.response,
      title: 'title.artists',
      start: start,
      end: end,
    };
  }
  catch (error) {
    console.error(error);
  }
};
