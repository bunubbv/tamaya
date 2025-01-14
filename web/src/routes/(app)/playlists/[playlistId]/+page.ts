import { getPlaylist } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const playListId: string = params.playListId

  try {
    const data = await getPlaylist(fetch, playListId);

    return {
      item: data.response!,
      title: data.response.playlist_name,
    };
  }
  catch (error) {
    console.error(error);
  }
};
