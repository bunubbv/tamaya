<script lang="ts">
  import '../style.css';
</script>


<div id="wrap">
  <slot />
</div>


<style>
  #wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--space-m);
    flex-direction: column;
  }
</style>