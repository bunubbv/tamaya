<script lang="ts">
  export let title: string;
  export let inline: boolean = false;
  export let size: string = 'xl';
</script>


{#if title}
  <div
    style:display={ inline ? 'inline' : ''}
    class:xl={ size == 'xl' }
    class:l={ size == 'l' }
  >
    <span>{title}</span>
  </div>
{/if}


<style>
  div {
    margin-bottom: 27px;
  }

  .xl {
    font-size: 32px;
  }

  .l {
    font-size: 24px;
  }

  span {
    font-weight: bolder;
    letter-spacing: -1px;
    line-height: 1;
  }
</style>
